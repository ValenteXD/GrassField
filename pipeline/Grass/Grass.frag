#version 400

//inputs
in float age;
in float height;
in vec2 textureCoord;

//uniforms
uniform int type;

//outputs
out vec4 color;

void main(){
    
    //convert age multiplyer to a range of 0 to 1 instead of 1 to 3
    float age0to1 = (age-1)/2;

    //coloring based on what point of the grass blade is being drawn and how old it is 
    color = vec4((vec3(0.0,0.7,0.2)*height)+(vec3(0.89,0.84,0.04)*age0to1*height), 1.0);
}