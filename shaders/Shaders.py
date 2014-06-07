class Shaders(object):
    def __init__(self):

        self.vertex_shader = """
        uniform sampler2D Texture0;
        uniform sampler2D Texture1;
        uniform sampler2D Texture2;
        varying vec3 N;
        varying vec3 v;
        varying vec4 vTexCoord0;
        varying vec4 vTexCoord1;
        varying vec4 vTexCoord2;
        void main(void)
        {
            vTexCoord0 = gl_MultiTexCoord0;
            vTexCoord1 = gl_MultiTexCoord1;
            vTexCoord2 = gl_MultiTexCoord2;

            N = normalize(gl_NormalMatrix * gl_Normal);

            v = vec3(gl_ModelViewMatrix * gl_Vertex);

            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

        }
        """
        self.fragment_shader = """
        varying vec3 N;
        varying vec3 v;

        void main (void)
        {
           N = -N
           vec3 L = normalize(gl_LightSource[0].position.xyz - v);
           vec3 E = normalize(v); // we are in Eye Coordinates, so EyePos is (0,0,0)
           vec3 R = normalize(reflect(L,N));

           //calculate Ambient Term:
           vec4 Iamb = gl_FrontLightProduct[0].ambient;

           //calculate Diffuse Term:
           vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0);
           Idiff = clamp(Idiff, 0.0, 1.0);

           // calculate Specular Term:
           vec4 Ispec = gl_FrontLightProduct[0].specular
                        * pow(max(dot(R,E),0.0),0.3*gl_FrontMaterial.shininess);
           Ispec = clamp(Ispec, 0.0, 1.0);

           // write Total Color:
           gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;
        }
        """""


        self.fragment_shader_multi = """
        uniform sampler2D Texture0;
        uniform sampler2D Texture1;
        uniform sampler2D Texture2;
        varying vec4 vTexCoord0;
        varying vec4 vTexCoord1;
        varying vec4 vTexCoord2;
        varying vec3 N;
        varying vec3 v;

        #define MAX_LIGHTS 2

        void main (void)
        {
           vec4 finalColor = vec4(0.0, 0.0, 0.0, 1.0);
           for (int i=0;i<MAX_LIGHTS;i++)
           {
              vec3 color = normalize(texture2D(Texture2, vTexCoord2.st).rgb);
              //float factor = ((color[0]*2.0)-1.0);
              float factor = (((0.30*color[0] + 0.59*color[1] + 0.11*color[2])*2.0)-1.0);
              vec3 nN = N;
              vec3 L = normalize(gl_LightSource[i].position.xyz - v);
              vec3 E = normalize(-v); // we are in Eye Coordinates, so EyePos is (0,0,0)
              vec3 R = normalize(-reflect(L,nN));

              //calculate Ambient Term:
              vec4 Iamb = gl_FrontLightProduct[i].ambient;

              //calculate Diffuse Term:
              vec4 Idiff = gl_FrontLightProduct[i].diffuse * max(dot(nN,L), 0.0);
              Idiff = clamp(Idiff, 0.0, 1.0);

              // calculate Specular Term:
              vec4 Ispec = gl_FrontLightProduct[i].specular
                     * pow(max(dot(R,E),0.0),0.3*gl_FrontMaterial.shininess);
              Ispec = clamp(Ispec, 0.0, 1.0);

              float a = gl_LightSource[i].constantAttenuation;
              float b = gl_LightSource[i].linearAttenuation;
              float c = gl_LightSource[i].quadraticAttenuation;
              float d = sqrt(pow(L.x,2) +pow(L.y,2) + pow(L.z,2)) ;

              vec4 texel = vec4(texture2D(Texture0, vTexCoord0.st).rgba);
              //finalColor += Iamb + (Idiff + Ispec)/ (a + b*d + d*c) + texel;
              finalColor += (Iamb + Idiff + Ispec)/ (a + b*d + d*c);
           }
           // write Total Color:
           gl_FragColor = gl_FrontLightModelProduct.sceneColor + finalColor;
        }
        """""

__author__ = 'bruno'
