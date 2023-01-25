from OpenGL import GL
from array import array
import ctypes
import glm
import math

class Terrain_old:

    def relevo(self,x,y):
        return x**2-y**2
    
    def __init__(self,n):
        self.n=n
        self.pi = math.pi
        d = 1.0/n
        position = array('f')
        for i in range(0,n):
            for j in range(0,n):
                x = i*d
                z = j*d
                y = self.relevo(x,z)
                nextX = (i+1)*d
                nextZ = (j+1)*d
                y2=self.relevo(nextX,z)
                y3=self.relevo(x,nextZ)
                y4=self.relevo(nextX,nextZ)
                
                position.append(x)
                position.append(y)
                position.append(z)

                position.append(x)
                position.append(y3)
                position.append(nextZ)

                position.append(nextX)
                position.append(y4)
                position.append(nextZ)

                position.append(nextX)
                position.append(y4)
                position.append(nextZ)
                
                position.append(nextX)
                position.append(y2)
                position.append(z)

                position.append(x)
                position.append(y)
                position.append(z)
                


        textureCoord = array('f')
        for i in range(0,n):
            for j in range(0,n):
                x=0.5+math.sin(i)/2
                y=0.5+math.sin(j)/2
                nextX=0.5+math.sin(i+1)/2
                nextY=0.5+math.sin(j+1)/2
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

        normal = array('f',[0.0,1.0,0.0]*(n**2)*6)

        self.squareArrayBufferId = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.squareArrayBufferId)
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glEnableVertexAttribArray(2)
        
        idVertexBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        idTextureBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textureCoord)*textureCoord.itemsize, ctypes.c_void_p(textureCoord.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        idNormalBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idNormalBuffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(normal)*normal.itemsize, ctypes.c_void_p(normal.buffer_info()[0]), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(2,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
    
    def draw(self,projection,camera,model):
        global posY
        global posX
        global posZ
        
        mvp = projection * camera * model
        normalMatrix = glm.transpose(glm.inverse(glm.mat3(camera*model)))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glUniformMatrix3fv(GL.glGetUniformLocation(self.pipeline, "normalMatrix"),1,GL.GL_FALSE,glm.value_ptr(normalMatrix))
        GL.glBindVertexArray(self.squareArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLES,0,(self.n**2)*6)

class Terrain:
    def __init__(self,n,size,pipeline):
        self.n=n
        dist=size/n
        self.pipeline=pipeline
        GL.glUniform1f(GL.glGetUniformLocation(pipeline,"size"),size)
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
            GL.glBindVertexArray(self.squareArrayBufferId)
            GL.glDrawArrays(GL.GL_TRIANGLES,0,(self.n**2)*6)