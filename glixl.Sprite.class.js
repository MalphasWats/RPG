var glixl = (function(glixl)
{
    glixl.Sprite = function Sprite(parameters)
    {
        this.x = parameters.x || 0;
        this.y = parameters.y || 0;
        this.z = parameters.z || 0;
        
        this.width = parameters.width || 16;
        this.height = parameters.height || 16;
        
        this.angle = parameters.angle || 0;
        this.scale = parameters.scale || 1;
        
        this.frame = parameters.frame || 0;
    }
    
    glixl.Sprite.prototype.update = function()
    {
        // TODO: Animation code goes here
        this.x += 1;
        if (this.x > 700)
            this.x = 0;
    }
    
    return glixl;
    
})(glixl || {});