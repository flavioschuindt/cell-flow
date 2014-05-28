class Shaders(object):
    def __init__(self):

        self.vertex_shader = """
        varying vec3 vertex_normal;
    void main()
    {
        vertex_normal = gl_Normal;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        vec3 light_direction = normalize(vec3(gl_LightSource[0].position));
        //float diffuse = max(0.0, dot(vertex_normal, light_direction));
        //gl_FrontColor = vec4(diffuse,diffuse,diffuse,1.0);
    }
"""
        self.fragment_shader = """
        varying vec3 vertex_normal;
    void main()
    {
        gl_FragColor = gl_Color;
    }
"""

__author__ = 'bruno'
