#version 400

//inputs
layout (location=0) in vec3 attr_position;
layout (location=1) in vec2 attr_textureCoord;

//uniforms
uniform mat4 MVP;
uniform sampler2D heightMap;
uniform float size;

//outputs
out vec2 textureCoord;

//samples the height map buffering it's color and then calculates it's brightness to be added to the y coordinate (height of the terrain)
float heightMapper(vec2 center){
    vec4 buffered_color = texture(heightMap,(attr_position.xz+center)/(4*size));
    return (size/4)*(buffered_color.x+buffered_color.y+buffered_color.z)/3;
}

void main(void) 
{
    //vector that recenters the terrain as compared to the height map 
    vec2 center = vec2(-size/2,-size/2);

    //geographical distortion
    float y = attr_position.y+heightMapper(center);

    //finilazes the position based on the MVP matrix and finalized coordinates
    gl_Position = MVP*vec4(attr_position.x,y,attr_position.z,1.0);
    
    //passes the received texture coordinates over to the fragment shader
    textureCoord = attr_textureCoord;
}
