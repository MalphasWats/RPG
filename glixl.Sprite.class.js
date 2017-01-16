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
        
        this.animations = { idle: { frames: [this.frame], frame_duration: 1000, frame_index: 0} };
        this.current_animation = this.animations['idle'];
        this.animation_timer = (new Date()).getTime();
    }
    
    glixl.Sprite.prototype.update = function()
    {
        // TODO: Animation code goes here
        //this.x += 1;
        //if (this.x > 700)
        //    this.x = 0;
        var ts = (new Date()).getTime();
        var delta = ts - this.animation_timer;
        //this.timestamp = ts;
        
        //console.log(ts, delta);

        if(delta > this.current_animation.frame_duration)
        {
            this.animation_timer = ts;
            
            this.current_animation.frame_index += 1;
            if (this.current_animation.frame_index >= this.current_animation.frames.length)
                this.current_animation.frame_index = 0;
            this.frame = this.current_animation.frames[this.current_animation.frame_index];
        }
        
        
    }
    
    glixl.Sprite.prototype.add_animation = function(name, frames, frame_duration)
    {
        this.animations[name] = { frames: frames, frame_duration: frame_duration, frame_index:0 };
    }
    
    glixl.Sprite.prototype.set_animation = function(name)
    {
        this.current_animation = this.animations[name];
        
        this.frame = this.current_animation.frames[this.current_animation.frame_index];
    }
    
    return glixl;
    
})(glixl || {});