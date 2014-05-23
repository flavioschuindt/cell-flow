"""
Some utility functions for using GLSL within an OpenGL python program.
"""

from OpenGL.GL import *
import sys

def compile_shader(source, shader_type):
    """Given a string containing the source for a GLSL shader
    of type shader_type (GL_VERTEX_SHADER or GL_FRAGMENT_SHADER), compiles
    it and returns the resulting shader identifier.
    """
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not status:
        print_log(shader)
        glDeleteShader(shader)
        raise ValueError, 'Shader compilation failed'
    return shader
    
def compile_program(vertex_source=None, fragment_source=None):
    """Compiles and links a vertex shader and/or a fragment shader and
    installs it/them for running.
    """
    
    program = glCreateProgram()
 
    if vertex_source:
        vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
        glAttachShader(program, vertex_shader)
    if fragment_source:
        fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragment_shader)
        
    glLinkProgram(program)
 
    return program
    
def print_log(shader):
    """Prints out error messages for the given shader object."""
    result = glGetShaderiv(shader, GL_INFO_LOG_LENGTH)
 
    if result > 0:
        log = glGetShaderInfoLog(shader)
        print >> sys.stderr, log

