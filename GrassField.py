from GLAPP import GLAPP
from OpenGL import GL
import glm
import math
from GrassBlade import *
from Terrain import *

DENSITY = 20
SIZE = 32
N = DENSITY*SIZE
DIST = 1/DENSITY

class InstancedGrass(GLAPP):
    def setup(self):
        # Window setup
        self.title("Grass Field")
        self.size(1920,1080)
        self.FPSlimit = 70

        # OpenGL Initialization
        GL.glClearColor(0.0212, 0.68, 0.83, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("Grass")
        self.pipelineTerrain=self.loadPipeline("Terrain")
        GL.glUseProgram(self.pipeline)


        #define wind speed and multiplyer for passage of time
        speed = 10.0
        self.timeMultiplyer = 1.0
        GL.glUniform1f(GL.glGetUniformLocation(self.pipeline,"speed"),speed)
        
        #Number of collumns for the array
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline,"collumn"),N)

        #Base distance between blades of grass
        GL.glUniform1f(GL.glGetUniformLocation(self.pipeline,"dist"),DIST)

        #Size of the grass field
        GL.glUniform1f(GL.glGetUniformLocation(self.pipeline,"size"),SIZE)

        #Textures and noise maps
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("./textures/displacementNoise.png")
        GL.glActiveTexture(GL.GL_TEXTURE1)
        self.loadTexture("./textures/heightMap.png")
        GL.glActiveTexture(GL.GL_TEXTURE2)
        self.loadTexture("./textures/Grass.png")
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline, "displacement"),0)
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline, "heightMap"),1)
        
        # Loading grass
        self.grass=GrassBlade(self.pipeline)

        # Switching to terrain pipeline

        GL.glUseProgram(self.pipelineTerrain)
        GL.glUniform1i(GL.glGetUniformLocation(self.pipelineTerrain, "terrainTexture"),2)
        GL.glUniform1i(GL.glGetUniformLocation(self.pipelineTerrain, "heightMap"),1)

        #Loading terrain
        GL.glUseProgram(self.pipelineTerrain)
        self.terrain = Terrain(N//10,SIZE,self.pipelineTerrain)

        #Define render distance
        self.renderDistance=100


    def draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,self.renderDistance)
        camera = glm.lookAt(glm.vec3(SIZE/2,SIZE/4,SIZE/2),glm.vec3(-SIZE/2,0,-SIZE/2),glm.vec3(0,1,0))
        model = glm.translate(glm.vec3(0,0,0))*glm.rotate(0,glm.vec3(0,1,0))

        mvp = projection*camera*model

        #Draw the terrain
        GL.glUseProgram(self.pipelineTerrain)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipelineTerrain, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        self.terrain.draw()

        #Draw the grass
        GL.glUseProgram(self.pipeline)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glUniform1f(GL.glGetUniformLocation(self.pipeline,"time"),self.passedTime)
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        self.grass.draw(N**2)

InstancedGrass()