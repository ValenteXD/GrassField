#version 400

//inputs
in vec2 textureCoord;

//uniforms
uniform sampler2D terrainTexture;

//outputs
out vec4 color;

void main(void) 
{
    //texture coordinate determines color based on the corresponding texture
    color = texture(terrainTexture,textureCoord);
}
