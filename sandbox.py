from enum import Enum
from collections import deque

# TODO: Preprocess unit clauses
# TODO: Process empty clause properly

input = """p cnf 329 952
-13 -5 0
-13 -6 0
5 6 13 0
-14 -4 0
-14 13 0
4 -13 14 0
-15 -3 0
-15 14 0
3 -14 15 0
-16 -2 0
-16 15 0
2 -15 16 0
-17 1 0
-17 16 0
-1 -16 17 0
-18 -11 0
-18 -12 0
11 12 18 0
-19 -10 0
-19 18 0
10 -18 19 0
-20 -9 0
-20 19 0
9 -19 20 0
-21 -8 0
-21 20 0
8 -20 21 0
-22 7 0
-22 21 0
-7 -21 22 0
-23 -17 0
-23 -22 0
17 22 23 0
-24 1 0
-24 7 0
-1 -7 24 0
-25 1 0
-25 8 0
-1 -8 25 0
-26 2 0
-26 7 0
-2 -7 26 0
-27 25 0
-27 26 0
-25 -26 27 0
-28 -25 0
-28 -26 0
25 26 28 0
-29 -27 0
-29 -28 0
27 28 29 0
-30 3 0
-30 7 0
-3 -7 30 0
-31 1 0
-31 9 0
-1 -9 31 0
-32 2 0
-32 8 0
-2 -8 32 0
-33 32 0
-33 -27 0
-32 27 33 0
-34 -32 0
-34 27 0
32 -27 34 0
-35 -33 0
-35 -34 0
33 34 35 0
-36 31 0
-36 -35 0
-31 35 36 0
-37 -31 0
-37 35 0
31 -35 37 0
-38 -36 0
-38 -37 0
36 37 38 0
-39 30 0
-39 38 0
-30 -38 39 0
-40 -30 0
-40 -38 0
30 38 40 0
-41 -39 0
-41 -40 0
39 40 41 0
-42 4 0
-42 7 0
-4 -7 42 0
-43 1 0
-43 10 0
-1 -10 43 0
-44 2 0
-44 9 0
-2 -9 44 0
-45 -31 0
-45 -32 0
31 32 45 0
-46 27 0
-46 -45 0
-27 45 46 0
-47 31 0
-47 32 0
-31 -32 47 0
-48 -46 0
-48 -47 0
46 47 48 0
-49 44 0
-49 48 0
-44 -48 49 0
-50 -44 0
-50 -48 0
44 48 50 0
-51 -49 0
-51 -50 0
49 50 51 0
-52 43 0
-52 -51 0
-43 51 52 0
-53 -43 0
-53 51 0
43 -51 53 0
-54 -52 0
-54 -53 0
52 53 54 0
-55 3 0
-55 8 0
-3 -8 55 0
-56 55 0
-56 -39 0
-55 39 56 0
-57 -55 0
-57 39 0
55 -39 57 0
-58 -56 0
-58 -57 0
56 57 58 0
-59 54 0
-59 -58 0
-54 58 59 0
-60 -54 0
-60 58 0
54 -58 60 0
-61 -59 0
-61 -60 0
59 60 61 0
-62 42 0
-62 61 0
-42 -61 62 0
-63 -42 0
-63 -61 0
42 61 63 0
-64 -62 0
-64 -63 0
62 63 64 0
-65 6 0
-65 7 0
-6 -7 65 0
-66 1 0
-66 12 0
-1 -12 66 0
-67 2 0
-67 10 0
-2 -10 67 0
-68 -43 0
-68 -44 0
43 44 68 0
-69 -48 0
-69 -68 0
48 68 69 0
-70 43 0
-70 44 0
-43 -44 70 0
-71 -69 0
-71 -70 0
69 70 71 0
-72 67 0
-72 71 0
-67 -71 72 0
-73 -67 0
-73 -71 0
67 71 73 0
-74 -72 0
-74 -73 0
72 73 74 0
-75 66 0
-75 -74 0
-66 74 75 0
-76 -66 0
-76 74 0
66 -74 76 0
-77 -75 0
-77 -76 0
75 76 77 0
-78 3 0
-78 9 0
-3 -9 78 0
-79 -55 0
-79 -54 0
55 54 79 0
-80 39 0
-80 -79 0
-39 79 80 0
-81 55 0
-81 54 0
-55 -54 81 0
-82 -80 0
-82 -81 0
80 81 82 0
-83 78 0
-83 82 0
-78 -82 83 0
-84 -78 0
-84 -82 0
78 82 84 0
-85 -83 0
-85 -84 0
83 84 85 0
-86 77 0
-86 -85 0
-77 85 86 0
-87 -77 0
-87 85 0
77 -85 87 0
-88 -86 0
-88 -87 0
86 87 88 0
-89 4 0
-89 8 0
-4 -8 89 0
-90 89 0
-90 -62 0
-89 62 90 0
-91 -89 0
-91 62 0
89 -62 91 0
-92 -90 0
-92 -91 0
90 91 92 0
-93 88 0
-93 -92 0
-88 92 93 0
-94 -88 0
-94 92 0
88 -92 94 0
-95 -93 0
-95 -94 0
93 94 95 0
-96 65 0
-96 95 0
-65 -95 96 0
-97 -65 0
-97 -95 0
65 95 97 0
-98 -96 0
-98 -97 0
96 97 98 0
-99 5 0
-99 7 0
-5 -7 99 0
-100 1 0
-100 11 0
-1 -11 100 0
-101 2 0
-101 12 0
-2 -12 101 0
-102 -66 0
-102 -67 0
66 67 102 0
-103 -71 0
-103 -102 0
71 102 103 0
-104 66 0
-104 67 0
-66 -67 104 0
-105 -103 0
-105 -104 0
103 104 105 0
-106 101 0
-106 105 0
-101 -105 106 0
-107 -101 0
-107 -105 0
101 105 107 0
-108 -106 0
-108 -107 0
106 107 108 0
-109 100 0
-109 -108 0
-100 108 109 0
-110 -100 0
-110 108 0
100 -108 110 0
-111 -109 0
-111 -110 0
109 110 111 0
-112 3 0
-112 10 0
-3 -10 112 0
-113 -78 0
-113 -77 0
78 77 113 0
-114 -82 0
-114 -113 0
82 113 114 0
-115 78 0
-115 77 0
-78 -77 115 0
-116 -114 0
-116 -115 0
114 115 116 0
-117 112 0
-117 116 0
-112 -116 117 0
-118 -112 0
-118 -116 0
112 116 118 0
-119 -117 0
-119 -118 0
117 118 119 0
-120 111 0
-120 -119 0
-111 119 120 0
-121 -111 0
-121 119 0
111 -119 121 0
-122 -120 0
-122 -121 0
120 121 122 0
-123 4 0
-123 9 0
-4 -9 123 0
-124 -89 0
-124 -88 0
89 88 124 0
-125 62 0
-125 -124 0
-62 124 125 0
-126 89 0
-126 88 0
-89 -88 126 0
-127 -125 0
-127 -126 0
125 126 127 0
-128 123 0
-128 127 0
-123 -127 128 0
-129 -123 0
-129 -127 0
123 127 129 0
-130 -128 0
-130 -129 0
128 129 130 0
-131 122 0
-131 -130 0
-122 130 131 0
-132 -122 0
-132 130 0
122 -130 132 0
-133 -131 0
-133 -132 0
131 132 133 0
-134 6 0
-134 8 0
-6 -8 134 0
-135 134 0
-135 -96 0
-134 96 135 0
-136 -134 0
-136 96 0
134 -96 136 0
-137 -135 0
-137 -136 0
135 136 137 0
-138 133 0
-138 -137 0
-133 137 138 0
-139 -133 0
-139 137 0
133 -137 139 0
-140 -138 0
-140 -139 0
138 139 140 0
-141 99 0
-141 140 0
-99 -140 141 0
-142 -99 0
-142 -140 0
99 140 142 0
-143 -141 0
-143 -142 0
141 142 143 0
-144 2 0
-144 11 0
-2 -11 144 0
-145 -100 0
-145 -101 0
100 101 145 0
-146 -105 0
-146 -145 0
105 145 146 0
-147 100 0
-147 101 0
-100 -101 147 0
-148 -146 0
-148 -147 0
146 147 148 0
-149 144 0
-149 -148 0
-144 148 149 0
-150 -144 0
-150 148 0
144 -148 150 0
-151 -149 0
-151 -150 0
149 150 151 0
-152 3 0
-152 12 0
-3 -12 152 0
-153 -112 0
-153 -111 0
112 111 153 0
-154 -116 0
-154 -153 0
116 153 154 0
-155 112 0
-155 111 0
-112 -111 155 0
-156 -154 0
-156 -155 0
154 155 156 0
-157 152 0
-157 156 0
-152 -156 157 0
-158 -152 0
-158 -156 0
152 156 158 0
-159 -157 0
-159 -158 0
157 158 159 0
-160 151 0
-160 -159 0
-151 159 160 0
-161 -151 0
-161 159 0
151 -159 161 0
-162 -160 0
-162 -161 0
160 161 162 0
-163 4 0
-163 10 0
-4 -10 163 0
-164 -123 0
-164 -122 0
123 122 164 0
-165 -127 0
-165 -164 0
127 164 165 0
-166 123 0
-166 122 0
-123 -122 166 0
-167 -165 0
-167 -166 0
165 166 167 0
-168 163 0
-168 167 0
-163 -167 168 0
-169 -163 0
-169 -167 0
163 167 169 0
-170 -168 0
-170 -169 0
168 169 170 0
-171 162 0
-171 -170 0
-162 170 171 0
-172 -162 0
-172 170 0
162 -170 172 0
-173 -171 0
-173 -172 0
171 172 173 0
-174 6 0
-174 9 0
-6 -9 174 0
-175 -134 0
-175 -133 0
134 133 175 0
-176 96 0
-176 -175 0
-96 175 176 0
-177 134 0
-177 133 0
-134 -133 177 0
-178 -176 0
-178 -177 0
176 177 178 0
-179 174 0
-179 178 0
-174 -178 179 0
-180 -174 0
-180 -178 0
174 178 180 0
-181 -179 0
-181 -180 0
179 180 181 0
-182 173 0
-182 -181 0
-173 181 182 0
-183 -173 0
-183 181 0
173 -181 183 0
-184 -182 0
-184 -183 0
182 183 184 0
-185 5 0
-185 8 0
-5 -8 185 0
-186 185 0
-186 -141 0
-185 141 186 0
-187 -185 0
-187 141 0
185 -141 187 0
-188 -186 0
-188 -187 0
186 187 188 0
-189 184 0
-189 -188 0
-184 188 189 0
-190 -184 0
-190 188 0
184 -188 190 0
-191 -189 0
-191 -190 0
189 190 191 0
-192 3 0
-192 11 0
-3 -11 192 0
-193 -152 0
-193 -151 0
152 151 193 0
-194 -156 0
-194 -193 0
156 193 194 0
-195 152 0
-195 151 0
-152 -151 195 0
-196 -194 0
-196 -195 0
194 195 196 0
-197 192 0
-197 196 0
-192 -196 197 0
-198 -192 0
-198 -196 0
192 196 198 0
-199 -197 0
-199 -198 0
197 198 199 0
-200 149 0
-200 -199 0
-149 199 200 0
-201 -149 0
-201 199 0
149 -199 201 0
-202 -200 0
-202 -201 0
200 201 202 0
-203 4 0
-203 12 0
-4 -12 203 0
-204 -163 0
-204 -162 0
163 162 204 0
-205 -167 0
-205 -204 0
167 204 205 0
-206 163 0
-206 162 0
-163 -162 206 0
-207 -205 0
-207 -206 0
205 206 207 0
-208 203 0
-208 207 0
-203 -207 208 0
-209 -203 0
-209 -207 0
203 207 209 0
-210 -208 0
-210 -209 0
208 209 210 0
-211 202 0
-211 -210 0
-202 210 211 0
-212 -202 0
-212 210 0
202 -210 212 0
-213 -211 0
-213 -212 0
211 212 213 0
-214 6 0
-214 10 0
-6 -10 214 0
-215 -174 0
-215 -173 0
174 173 215 0
-216 -178 0
-216 -215 0
178 215 216 0
-217 174 0
-217 173 0
-174 -173 217 0
-218 -216 0
-218 -217 0
216 217 218 0
-219 214 0
-219 218 0
-214 -218 219 0
-220 -214 0
-220 -218 0
214 218 220 0
-221 -219 0
-221 -220 0
219 220 221 0
-222 213 0
-222 -221 0
-213 221 222 0
-223 -213 0
-223 221 0
213 -221 223 0
-224 -222 0
-224 -223 0
222 223 224 0
-225 5 0
-225 9 0
-5 -9 225 0
-226 -185 0
-226 -184 0
185 184 226 0
-227 141 0
-227 -226 0
-141 226 227 0
-228 185 0
-228 184 0
-185 -184 228 0
-229 -227 0
-229 -228 0
227 228 229 0
-230 225 0
-230 229 0
-225 -229 230 0
-231 -225 0
-231 -229 0
225 229 231 0
-232 -230 0
-232 -231 0
230 231 232 0
-233 224 0
-233 -232 0
-224 232 233 0
-234 -224 0
-234 232 0
224 -232 234 0
-235 -233 0
-235 -234 0
233 234 235 0
-236 -192 0
-236 -149 0
192 149 236 0
-237 -196 0
-237 -236 0
196 236 237 0
-238 192 0
-238 149 0
-192 -149 238 0
-239 -237 0
-239 -238 0
237 238 239 0
-240 4 0
-240 11 0
-4 -11 240 0
-241 -203 0
-241 -202 0
203 202 241 0
-242 -207 0
-242 -241 0
207 241 242 0
-243 203 0
-243 202 0
-203 -202 243 0
-244 -242 0
-244 -243 0
242 243 244 0
-245 240 0
-245 244 0
-240 -244 245 0
-246 -240 0
-246 -244 0
240 244 246 0
-247 -245 0
-247 -246 0
245 246 247 0
-248 -239 0
-248 -247 0
239 247 248 0
-249 239 0
-249 247 0
-239 -247 249 0
-250 -248 0
-250 -249 0
248 249 250 0
-251 6 0
-251 12 0
-6 -12 251 0
-252 -214 0
-252 -213 0
214 213 252 0
-253 -218 0
-253 -252 0
218 252 253 0
-254 214 0
-254 213 0
-214 -213 254 0
-255 -253 0
-255 -254 0
253 254 255 0
-256 251 0
-256 255 0
-251 -255 256 0
-257 -251 0
-257 -255 0
251 255 257 0
-258 -256 0
-258 -257 0
256 257 258 0
-259 250 0
-259 -258 0
-250 258 259 0
-260 -250 0
-260 258 0
250 -258 260 0
-261 -259 0
-261 -260 0
259 260 261 0
-262 5 0
-262 10 0
-5 -10 262 0
-263 -225 0
-263 -224 0
225 224 263 0
-264 -229 0
-264 -263 0
229 263 264 0
-265 225 0
-265 224 0
-225 -224 265 0
-266 -264 0
-266 -265 0
264 265 266 0
-267 262 0
-267 266 0
-262 -266 267 0
-268 -262 0
-268 -266 0
262 266 268 0
-269 -267 0
-269 -268 0
267 268 269 0
-270 261 0
-270 -269 0
-261 269 270 0
-271 -261 0
-271 269 0
261 -269 271 0
-272 -270 0
-272 -271 0
270 271 272 0
-273 -240 0
-273 239 0
240 -239 273 0
-274 -244 0
-274 -273 0
244 273 274 0
-275 240 0
-275 -239 0
-240 239 275 0
-276 -274 0
-276 -275 0
274 275 276 0
-277 6 0
-277 11 0
-6 -11 277 0
-278 -251 0
-278 -250 0
251 250 278 0
-279 -255 0
-279 -278 0
255 278 279 0
-280 251 0
-280 250 0
-251 -250 280 0
-281 -279 0
-281 -280 0
279 280 281 0
-282 277 0
-282 281 0
-277 -281 282 0
-283 -277 0
-283 -281 0
277 281 283 0
-284 -282 0
-284 -283 0
282 283 284 0
-285 -276 0
-285 -284 0
276 284 285 0
-286 276 0
-286 284 0
-276 -284 286 0
-287 -285 0
-287 -286 0
285 286 287 0
-288 5 0
-288 12 0
-5 -12 288 0
-289 -262 0
-289 -261 0
262 261 289 0
-290 -266 0
-290 -289 0
266 289 290 0
-291 262 0
-291 261 0
-262 -261 291 0
-292 -290 0
-292 -291 0
290 291 292 0
-293 288 0
-293 292 0
-288 -292 293 0
-294 -288 0
-294 -292 0
288 292 294 0
-295 -293 0
-295 -294 0
293 294 295 0
-296 287 0
-296 -295 0
-287 295 296 0
-297 -287 0
-297 295 0
287 -295 297 0
-298 -296 0
-298 -297 0
296 297 298 0
-299 -288 0
-299 -287 0
288 287 299 0
-300 -292 0
-300 -299 0
292 299 300 0
-301 288 0
-301 287 0
-288 -287 301 0
-302 -300 0
-302 -301 0
300 301 302 0
-303 5 0
-303 11 0
-5 -11 303 0
-304 -277 0
-304 276 0
277 -276 304 0
-305 -281 0
-305 -304 0
281 304 305 0
-306 277 0
-306 -276 0
-277 276 306 0
-307 -305 0
-307 -306 0
305 306 307 0
-308 -303 0
-308 307 0
303 -307 308 0
-309 -302 0
-309 -308 0
302 308 309 0
-310 303 0
-310 -307 0
-303 307 310 0
-311 -309 0
-311 -310 0
309 310 311 0
-312 303 0
-312 302 0
-303 -302 312 0
-313 -303 0
-313 -302 0
303 302 313 0
-314 -312 0
-314 -313 0
312 313 314 0
-315 -307 0
-315 -314 0
307 314 315 0
-316 307 0
-316 314 0
-307 -314 316 0
-317 -315 0
-317 -316 0
315 316 317 0
-318 311 0
-318 -317 0
-311 317 318 0
-319 -298 0
-319 318 0
298 -318 319 0
-320 -272 0
-320 319 0
272 -319 320 0
-321 -235 0
-321 320 0
235 -320 321 0
-322 191 0
-322 321 0
-191 -321 322 0
-323 143 0
-323 322 0
-143 -322 323 0
-324 98 0
-324 323 0
-98 -323 324 0
-325 64 0
-325 324 0
-64 -324 325 0
-326 -41 0
-326 325 0
41 -325 326 0
-327 -29 0
-327 326 0
29 -326 327 0
-328 24 0
-328 327 0
-24 -327 328 0
-329 23 0
-329 328 0
-23 -328 329 0
329 0"""

TruthValue = Enum('TruthValue', ['TRUE', 'FALSE', 'UNASSIGNED'])

# First data structure: queue of literals to propagate
to_propagate = deque()

# Second data structure: current assignment
assignment = []

# Third data structure: model of current assignment
model = []

# Fourth data structure: list of literals, each pointing to a list of clauses watching that literal
literals_with_watching_clauses = []

# Fifth data structure: set of clauses
clauses = []

decision_level = 0

# Debug printing function
def print_global_state():
  print("to_propagate: ", to_propagate)
  print_assignment()
  print("model: ", end="")
  for i, val in enumerate(model, start=1):
    print(i, ": ", val, "; ", end="")
  print()
  print("literals_with_watching_clauses: ", literals_with_watching_clauses)
  print()
  
def preprocess():
  for clause in clauses[1:]:
    if len(clause) == 1:
      to_propagate.append(abs(int(clause[0])))
  
def print_assignment():
  print("assignment: ", end="")
  for val in assignment:
    print(f"(literal: {val[0]}, decision_level: {val[1]}) ", end="")
  print()

# Initialization function for our core data structures
def initialize_data_structures(input):
  input = input.split('\n')
  input = [line.split() for line in input]
  num_variables = int(input[0][2])
  num_clauses = int(input[0][3])
  print("----- INITIALIZING GLOBAL STATE -----\n")
  print("input: ", input)
  print("number of variables: ", num_variables)
  print("number of clauses: ", num_clauses) 

  for i in range(1, num_clauses+1):
    if (not input[i][:-1]):
      print("UNSAT")
      exit()
    if (input[i]):
      clauses.append(input[i][:-1])

  print("clauses: ", clauses, end="\n\n")
  
  for i in range(1, num_variables+1):
    model.append(TruthValue.UNASSIGNED)

    watching_clauses_pos = []
    watching_clauses_neg = []

    for j, clause in enumerate(clauses, start=1):
      if (int(clause[0]) == i):
        watching_clauses_pos.append(int(j))
      elif (len(clause) > 1 and int(clause[1]) == i): # TODO: Make more efficient
        watching_clauses_pos.append(int(j))
      elif (int(clause[0]) == -1*i):
        watching_clauses_neg.append(int(j))
      elif (int(len(clause) > 1 and clause[1]) == -1*i): # TODO: Make more efficient
        watching_clauses_neg.append(int(j))

    literals_with_watching_clauses.append((i, watching_clauses_pos))
    literals_with_watching_clauses.append((-1*i, watching_clauses_neg))

# Decide rule. Pick an unassigned literal, give it a random truth value, 
# and update our data structures accordingly.
def decide():
  print("----- EXECUTING DECIDE RULE -----\n")
  global decision_level
  
  # Update model, queue of literals to propagate, and current assignment
  for i in range(len(model)):
    if (model[i] == TruthValue.UNASSIGNED):
      # For now, we are always guessing TRUE initially
      to_propagate.append(i+1)
      decision_level += 1

      # Increase decision level by 1, starting at 0

      #assignment.append((i+1, get_decision_level() + 1)) 
      print_global_state()
      return
    
  # If no variable to decide on, the problem is SAT
  print("SAT")
  exit()

# We have falsified old_lit (watched by clause) and therefore need to update clause's
# watched literals. We look for another literal to watch. If one exists, we swap it 
# with old_lit and return None. If not, we return the other watch 
# literal (which may spur a conflict or a new propagation).
def update_watched_literals(clause_number, clause, old_lit):
  if int(clause[0]) == -1*old_lit:
    old_lit_index = 0 
  else:
    old_lit_index = 1

  for i in range(2, len(clause)):
    j = abs(int(clause[i])) - 1
    if (int(clause[i]) > 0 and model[j] != TruthValue.FALSE) or (int(clause[i]) < 0 and model[j] != TruthValue.TRUE):
      clause[old_lit_index], clause[i] = clause[i], clause[old_lit_index]
      
      # Update literals_with_watching_clauses. This clause is no longer watching old_lit,
      # and starts watching new_lit
      new_lit = int(clause[i])
      literals_with_watching_clauses[compute_lit_index(old_lit)][1].remove(clause_number)
      literals_with_watching_clauses[compute_lit_index(new_lit)][1].append(clause_number)
      return None

  # We failed to find a new literal to watch
  try: # This fails for unit clauses
    return int(clause[(old_lit_index + 1) % 2])
  except:
    return None
  
def compute_lit_index(curr_lit):
  if curr_lit > 0:
    return curr_lit * 2 - 1
  else:
    return -1 * curr_lit * 2 - 2


# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
def propagate():
  while to_propagate:
    print("----- EXECUTING PROPAGATE RULE -----\n")
    curr_lit = to_propagate.popleft()
    
    # Update the current assignment and model with the literal we're propagating
    assignment.append((curr_lit, decision_level))
    if curr_lit > 0:
      if model[curr_lit-1] == TruthValue.FALSE:
        backtrack()
      else:
        model[curr_lit-1] = TruthValue.TRUE
    else:
      if model[-1*curr_lit-1] == TruthValue.TRUE:
        backtrack()
      else:
        model[-1*curr_lit - 1] = TruthValue.FALSE 

    # Update watched literals of all clauses watching the complement of curr_lit.
    # For these clauses, we either (i) find a new literal to watch, or 
    #                              (ii) add the other watched literal to to_propagate
    curr_lit_comp_index = compute_lit_index(curr_lit)
    
    for clause_index in literals_with_watching_clauses[curr_lit_comp_index][1]: 
      lit_to_prop = update_watched_literals(clause_index, clauses[clause_index-1], curr_lit)
      # If we cannot find a new literal to watch for some clause,
      # we look at the __other__ watched literal. If it is true, no action is needed.
      # If it is unassigned, we propagate it. If it is false, we have a conflict.
      if lit_to_prop:
        if model[abs(lit_to_prop) - 1] == TruthValue.UNASSIGNED:
          to_propagate.append(lit_to_prop)
        elif model[abs(lit_to_prop) - 1] == TruthValue.FALSE:
          backtrack()
          return
          
    print_global_state()
    
# Backtracking function. Update assignment and model.
def backtrack():
  print("----- EXECUTING BACKTRACK RULE -----\n")
  global decision_level
  global to_propagate
  
  to_propagate = deque()
 
  # Clear assignment up to the most recent decision
  for i, val in reversed(list(enumerate(assignment))):
    if (i == 0) or (assignment[i-1][1] != decision_level):
      break
    else: 
      assignment.pop()
      model[val[1]] = TruthValue.UNASSIGNED
    
  # If there is no decision to flip, fail
  if assignment[-1][1] == 0:
    print("UNSAT")
    exit()
  # Flip the last decision and update the decision level  
  assignment[-1] = (-1 * assignment[-1][0], assignment[-1][1] - 1) 
  decision_level = assignment[-1][1]
  if model[abs(assignment[-1][0]) - 1] == TruthValue.TRUE:
    model[abs(assignment[-1][0]) - 1] = TruthValue.FALSE;
  else:
    model[abs(assignment[-1][0]) - 1] = TruthValue.TRUE
 
def main():    
  initialize_data_structures(input)
  #preprocess()
  while True:
    propagate()
    decide()

main()
