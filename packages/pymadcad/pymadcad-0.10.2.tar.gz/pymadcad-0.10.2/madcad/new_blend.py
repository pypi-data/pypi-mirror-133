
from .mathutils import *
from .mesh import Mesh, Web, Wire, connpp, connpe
from .triangulation import TriangulationError

	
def blend(interfaces, center=None, tangents='tangent', weight=1., resolution=None):
	''' blending surface between wires '''
	indev
	
def junction(interfaces, center=None, tangents='tangent', weight=1., resolution=None):
	indev

	
def web_junction(interfaces, center=None, tangents='tangent', weight=1., resolution=None):
	''' junction between webs curves '''
	indev

def mesh_junction(interfaces, center=None, tangents='tangent', weight=1., resolution=None):
	''' junction between surface meshes '''
	pts, tangents, weights, loops = get_interfaces(args, tangents, weight)
	
	# get a web of everything
	pool = Web(pts, [])
	for loop in loops:
		pool.edges.extend((loop[i-1], loop[i])  for i in range(len(loop)))
	# determine the center if not given
	if not center:
		center = pool.barycenter()
	# project the points on a sphere
	dirs = pool.points = [normalize(p-center)  for p in pts]
	
	# find bridges to join loops
	clusters = [set(loop) for loop in loops]
	def contaning_loop(p):
		return next(i  for i,c in enumerate(clusters) if b in c)
		
	links = {}
	for bridge in line_bridges(pool):
		link = edgekey(containing_loop(bridge[0]), containing_loop(bridge[1]))
		links[link] = bridge
			
	
	# triangulate the sphere to know what portion belongs to which bridge
	for area in sphere_loops(pool, center):
		match = sphere_triangulation_outline(area)
		# find shortest missing links
		for edge in match.edges():
			link = (containing_loop(edge[0]), containing_loop(edge[1]))
			current = link[link]
			if distance2(dirs[edge[0]], dirs[edge[1]]) < distance2(dirs[current[0]], dirs[current[1]]):
				links[link] = edge
				
	
	
	
def sphere_triangulation_outline(outline: Web):
	''' triangulation outline working on a sphere, its center is 0 '''
	indev
	
def line_bridges(outline: Web):
	indev
	
def sphere_loops(outline: Web, center):
	return surface_loops(outline, lambda p: p-center)
	
	
# just for tests
def sphere_triangulation_closest(outline: Web, center=None, prec=None):
	''' triangulate an outline on a sphere '''
	if isinstance(outline, Wire):
		return sphere_triangulation_outline(outline, center, prec)
	else:
		outline = web(outline)
	
	result = Mesh(outline.points)
	# make all the line islands in outline a single outline, then find loops
	for loop in sphere_loops(outline + line_bridges(outline), center):
		# triangulate each loop
		result += sphere_triangulation_outline(loop, center, prec)
	return result

def sphere_triangulation_outline(outline: Wire, center, prec=None) -> Mesh:	
	if not center:		
		center = outline.barycenter()
	return triangulation_outline(outline, lambda p: p-center, prec)

def triangulation_outline(outline: Wire, normal: callable, prec=None) -> Mesh:
	''' return a mesh with the triangles formed in the outline
		the returned mesh uses the same buffer of points than the input
		
		normal(point) -> normal
		
		complexity:  O(n*k)  where k is the number of non convex points
	'''
	# get a normal in the right direction for loop winding
	if prec is None:	
		prec = outline.precision() **2
	
	# reducing contour
	pts = outline.points
	hole = list(outline.indices)
	if length2(pts[hole[-1]]-pts[hole[0]]) <= prec:		
		hole.pop()
	
	# set of remaining non-convexity points, indexing proj
	l = len(hole)
	nonconvex = { hole[i]
					for i in range(len(hole))
					if dot(cross(pts[hole[i]]-pts[hole[i-1]], pts[hole[(i+1)%l]]-pts[hole[i]]), normal(pts[hole[i]])) <= prec
					}
	
	def priority(u,v):
		''' priority criterion for 2D triangles, depending on its shape
		'''
		uv = length(u)*length(v)
		if not uv:	return 0
		return dot(u,v) / uv
	
	def score(i):
		l = len(hole)
		o = pts[hole[ i ]]
		u = pts[hole[ (i+1)%l ]] - o
		v = pts[hole[ (i-1)%l ]] - o
		surf = dot(cross(u,v), normal(o))
		triangle = (hole[(i-1)%l], hole[i], hole[(i+1)%l])
		
		# check for badly oriented triangle
		if surf < -prec:		return -inf
		# check for intersection with the rest
		if surf > prec:
			# check that there is not point of the outline inside the triangle
			for j in nonconvex:
				if j not in triangle:
					for k in range(3):
						o = pts[triangle[k]]
						if dot(pts[j]-o, cross(normal(o), o-pts[triangle[k-1]])) <= prec:
							break
					else:
						return -inf
		return priority(u,v)
	scores = [score(i) for i in range(len(hole))]
	
	triangles = []
	while len(hole) > 2:
		l = len(hole)
		i = imax(scores)
		if scores[i] == -inf:
			raise TriangulationError("no more feasible triangles (algorithm failure or bad input outline)", hole)
		triangles.append((
			hole[(i-1)%l], 
			hole[i], 
			hole[(i+1)%l],
			))
		nonconvex.discard(hole.pop(i))
		scores.pop(i)
		l -= 1
		scores[(i-1)%l] = score((i-1)%l)
		scores[i%l] = score(i%l)
	
	return Mesh(outline.points, triangles)


def line_bridges(lines: Web, conn=None) -> 'Web':
	''' find what edges to insert in the given mesh to make all its loops connex.
		returns a Web of the bridging edges.
		
		complexity:  O(n**2 + n*k)
		with
			n = number of points in the lines
			k = average number of points per loop
	'''
	if conn is None:	conn = connpe(lines.edges)
	pts = lines.points
	
	bridges = []	# edges created
	# reached and remaining parts, both as edge indices and point indices
	reached_points = {}	# closest to each reached point
	reached_edges = {}	# closest to each reached edge
	remain_points = set(p 	 for e in lines.edges for p in e)
	remain_edges = set(range(len(lines.edges)))
	
	def propagate(start):
		''' propagate from the given start point to make connex points and edges as reached '''
		front = [start]
		while front:
			s = front.pop()
			if s in reached_points:	continue
			reached_points[s] = (inf, (s,s))
			remain_points.discard(s)
			for e in conn[s]:
				if e in reached_edges: continue
				reached_edges[e] = (inf, (s,s))
				remain_edges.discard(e)
				front.extend(lines.edges[e])
				
	def update_closest():
		# from points to edges
		for s, (score, best) in reached_points.items():
			if best[0] in reached_points:
				reached_points[s] = find_closest_point(s)
		# from edges to points
		for e, (score, best) in reached_edges.items():
			if best[0] in reached_points:
				reached_edges[e] = find_closest_edge(e)
	
	def find_closest_edge(ac):
		''' find the bridge to the closest point to the given edge
		'''
		best = None
		score = inf
		# minimum from edge to points
		ep = lines.edgepoints(ac)
		for ma in remain_points:
			d = distance_pe(pts[ma], ep)
			if d < score:
				e = lines.edges[ac]
				if distance2(pts[ma], pts[e[0]]) < distance2(pts[ma], pts[e[1]]):
					score, best = d, (ma, e[0])
				else:
					score, best = d, (ma, e[1])
		
		return score, best
		
	def find_closest_point(ac):
		''' find the bridge to the closest edge to the given point
		'''
		best = None
		score = inf
		# minimum from point to edges
		for ma in remain_edges:
			d = distance_pe(pts[ac], lines.edgepoints(ma))
			if d < score:
				e = lines.edges[ma]
				if distance2(pts[ac], pts[e[0]]) < distance2(pts[ac], pts[e[1]]):
					score, best = d, (e[0], ac)
				else:
					score, best = d, (e[1], ac)
						
		return score, best
	
	# main loop
	propagate(lines.edges[0][0])
	while remain_edges:
		update_closest()
		closest = min(
					min(reached_points.values(), key=itemgetter(0)),
					min(reached_edges.values(), key=itemgetter(0)),
					key=itemgetter(0)) [1]
		bridges.append(closest)
		bridges.append(tuple(reversed(closest)))
		propagate(closest[0])
		
	return Web(lines.points, bridges)

		
def surface_loops(lines: Web, normal: callable) -> '[Wire]':
	''' collect the closed loops present in the given web, so that no loop overlap on the other ones.
	'''
	pts = lines.points
	# create an oriented point to edge connectivity 
	conn = Asso()
	for i,e in enumerate(lines.edges):
		conn.add(e[0], i)
	
	used = [False]*len(lines.edges)	# edges used and so no to use anymore
	loops = []
	
	# while there is edges remaining
	while True:
		# find an unused edge
		end = next((i  for i,u in enumerate(used) if not u), None)
		if end is None:
			break
		
		# assemble a loop
		loop = list(lines.edges[end])
		while True:
			# take the most inward next edge
			prev = normalize(pts[loop[-1]] - pts[loop[-2]])
			
			best = None
			score = -inf
			for edge in conn[loop[-1]]:
				if used[edge]:	continue
				e = lines.edges[edge]
				dir = normalize(pts[e[1]] - pts[e[0]])
				if isfinite(dir) and isfinite(prev):
					angle = atan2(
								dot(cross(prev,dir), normal(pts[e[0]])), 
								dot(prev,dir))
				else:
					angle = -pi
				if pi-angle < NUMPREC:	angle -= 2*pi
				if angle > score:
					score, best = angle, edge
			
			# progress on the selected edge
			if best is None:
				raise TriangulationError("there is not only loops in that web", loop)
			used[best] = True
			# stop when the best continuation is the start
			if best == end:
				break
			loop.append(lines.edges[best][1])
			
			
		loops.append(Wire(lines.points, loop))

	return loops
