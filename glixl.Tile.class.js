var glixl = (function(glixl)
{
    glixl.Tile = function Tile(parameters)
    {
        this.x = parameters.x || 0;
        this.y = parameters.y || 0;
        this.z = parameters.z || 0;
        
        this.width = parameters.width || 16;
        this.height = parameters.height || 16;
        
        this.frame = parameters.frame || 0;
    }
    
    glixl.Tile.prototype.update = function()
    {
        
    }
    
    glixl.Tile.prototype.use = function()
    {
        
    }
    
    return glixl;
    
})(glixl || {});