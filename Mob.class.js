var Mob = function(parameters)
{   
    glixl.Sprite.call(this, parameters);
    
    this.destination = false;
    this.path = [];
    
    this.speed = parameters.speed || 100;
    this.move_timer = (new Date()).getTime();
    
    this.home = parameters.home || [];
}

Mob.prototype.update = function()
{
    if (this.destination)
    {
        if (this.x == this.destination.x && this.y == this.destination.y)
        {
            if (this.path.length > 0)
            {
                this.destination = this.path.shift()
                this.destination.x += (this.width/2) * this.scale;
                this.destination.y += (this.height/4) * this.scale;
            }
            else
            {
                this.destination = false
            }
        }
    }
    
    this.move();
    this.redraw = true;
}

Mob.prototype.move = function()
{
    var now = (new Date()).getTime();
        
    var vx = 0
    var vy = 0
    
    if(this.x > this.destination.x)
        vx = -1;
    else if (this.x < this.destination.x)
        vx = 1;
        
    if(this.y > this.destination.y)
        vy = -1;
    else if (this.y < this.destination.y)
        vy = 1;
    
    
	var delta = now - this.move_timer;
	
	var dx = Math.abs(this.x - this.destination.x);
	var next_step = Math.round(vx * (delta / 1000 * this.speed));
	if (dx < Math.abs(next_step))
	    next_step = dx*vx;
	    
	this.x += next_step;
	
	var dy = Math.abs(this.y - this.destination.y);
	var next_step = Math.round(vy * (delta / 1000 * this.speed));
	if (dy < Math.abs(next_step))
	    next_step = dy*vy;
	
	this.y += next_step;
	
	this.move_timer = now;
}

Mob.prototype.set_path = function(path)
{
    if (path.length > 0)
    {
        this.path = path;
        this.destination = this.path.shift();
        this.destination.x += (this.width/2) * this.scale;
        this.destination.y += (this.height/4) * this.scale;
    }
}

Mob.prototype.clear_path = function()
{
    this.path = [];
    this.destination = false;
}

extend(glixl.Sprite, Mob);