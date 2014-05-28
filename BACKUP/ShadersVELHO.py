class ShadersVELHO(object):
    def __init__(self):

        self.vertex_shaderVelho = """
    varying vec3 vertex_normal;
    varying vec3 half_vector;
    varying vec3 v;
    varying vec4 bumpText;
    varying vec4 diffText;
    void main()
    {
        diffText        = gl_MultiTexCoord0;
        bumpText        = gl_MultiTexCoord1;
        vertex_normal   = normalize(gl_NormalMatrix * gl_Normal);
        half_vector     = normalize(vec3(gl_LightSource[0].halfVector));
        gl_Position     = gl_ModelViewProjectionMatrix * gl_Vertex;
        v               = vec3(gl_ModelViewMatrix * gl_Vertex);
    }
"""


        self.fragment_shaderVelho = """
    varying vec3 vertex_normal;
    varying vec3 half_vector;
    varying vec3 v;
    uniform sampler2D Texture0;
    uniform sampler2D Texture1;
    varying vec4 bumpText;
    varying vec4 diffText;
    void main()
    {
        //vec3 light_direction = normalize(vec3(gl_LightSource[0].position.xyz - v));

        vec3 vn = vertex_normal - normalize(vec3(texture2D(Texture1, bumpText.st).rgb));

        vec3 L = normalize(gl_LightSource[0].position.xyz - v);
        vec3 E = normalize(v);
        vec3 R = normalize(2.0 * vn * dot(L, vertex_normal) - L);

        //calculate Ambient Term:
        vec4 Iamb = gl_FrontLightProduct[0].ambient;

       //calculate Diffuse Term:

        vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(vn,L), 0.0);
        Idiff = clamp(Idiff, 0.0, 1.0);

        // calculate Specular Term:
        vec4 Ispec = gl_FrontLightProduct[0].specular * pow(max(dot(R, E), 0.0), 0.3 * gl_FrontMaterial.shininess);
        Ispec = clamp(Ispec, 0.0, 1.0);

        // write Total Color:
        //FALTA COLOCAR ATENUACAO
        vec4 texel = normalize(vec4(texture2D(Texture0, diffText.st).rgba));
        //gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec + texel;
        gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;
    }
"""

__author__ = 'bruno'
