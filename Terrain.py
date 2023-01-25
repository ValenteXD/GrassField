from OpenGL import GL
from array import array
import ctypes

class Terrain:
    def __init__(self,n,size,pipeline):
        # Defining number of vertices and distancing between them
        self.n=n
        dist=size/n
        self.pipeline=pipeline
        GL.glUniform1f(GL.glGetUniformLocation(pipeline,"size"),size)
        #Defining vertices for the mesh
        position = array('f')
        for i in range(n):
            for j in range(n):
                x = i*dist-size/2
                z = j*dist-size/2
                nextX=(i+1)*dist-size/2
                nextZ=(j+1)*dist-size/2

                position.append(x)
                position.append(0)
                position.append(z)

                position.append(x)
                position.append(0)
                position.append(nextZ)

                position.append(nextX)
                position.append(0)
                position.append(nextZ)

                position.append(nextX)
                position.append(0)
                position.append(nextZ)
                
                position.append(nextX)
                position.append(0)
                position.append(z)

                position.append(x)
                position.append(0)
                position.append(z)
        # Atributing coordinates for visual texture sampling (doesn't affect height map in any way)
        textureCoord = array('f')
        for i in range(n):
            for j in range(n):
                x=i*3
                y=j*3
                nextX=(i+1)*3
                nextY=(j+1)*3
                textureCoord.append(x)
                textureCoord.append(y)

                textureCoord.append(nextX)
                textureCoord.append(y)
                
                textureCoord.append(nextX)
                textureCoord.append(nextY)
                
                textureCoord.append(nextX)
                textureCoord.append(nextY)
                
                textureCoord.append(x)
                textureCoord.append(nextY)
                
                textureCoord.append(x)
                textureCoord.append(y)

            self.squareArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.squareArrayBufferId)
            GL.glEnableVertexAttribArray(0)# POSITION
            GL.glEnableVertexAttribArray(1)# TEXTURE COORDINATES
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idTextureBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textureCoord)*textureCoord.itemsize, ctypes.c_void_p(textureCoord.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))



    def draw(self):
        # Binding vertex array due to pipeline swapping then performs a draw call for the terrain
        GL.glBindVertexArray(self.squareArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLES,0,(self.n**2)*6)