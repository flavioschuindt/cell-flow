class Shaders(object):
    def __init__(self):

        self.vertex_shader = """
        varying vec3 vertex_normal;
        varying vec3 vertex;
        varying vec3 half_vector;
    void main()
    {
        vertex_normal = normalize(gl_NormalMatrix * gl_Normal);
        half_vector = normalize(vec3(gl_LightSource[0].halfVector));
        vertex = vec3(gl_ModelViewMatrix * gl_Vertex);
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

    }
"""
        self.fragment_shader = """
        varying vec3 vertex_normal;
        varying vec3 vertex;
        varying vec3 half_vector;
    void main()
    {
        vec3 L = vec3(gl_LightSource[0].position.xyz - vertex);
        vec3 N = normalize(vertex_normal);
        vec3 E = normalize(vertex);
        vec3 R = vec3(2.0*dot(L, N)*N - L);

        //AMBIENT
        vec4 Ia = normalize(gl_FrontLightProduct[0].ambient); // Luz ambiente atenuada pelo material

        //DIFFUSE
        vec4 Id = gl_FrontLightProduct[0].diffuse * max(dot(N, L),0.0 );
        Id = clamp(Id, 0.0, 1.0);

        //SPECULAR
        vec4 Is = gl_FrontLightProduct[0].specular * pow(max(dot(R, E), 0.0), 0.3 * gl_FrontMaterial.shininess);
        Is = clamp(Is, 0.0, 1.0);

        gl_FragColor = gl_FrontLightModelProduct.sceneColor + Ia + Id + Is;
    }
"""

__author__ = 'bruno'
