var Wiz = function(parameters)
{
    parameters.speed = 128;
    glixl.Sprite.call(this, parameters);
    
    /*this.label = document.createElement('span');
    this.label.innerHTML = parameters.name || 'Jeff';
    
    this.label.style.position = 'absolute';
    this.label.style.top = '0px';
    this.label.style.left = '0px';
    
    document.getElementsByTagName('body')[0].appendChild(this.label);*/
    
    this.light = new glixl.Light({x: this.x, y: this.y, radius:80, colour: [0.7, 0.7, 0.85]});
}

Wiz.prototype.update = function()
{
    glixl.Sprite.prototype.update.call(this);
    
    var destination = my_game.event_queue[0];
    
    if (destination)
    {
        this.path = my_game.scene.find_path(this, destination);
        this.path.shift(); // first coords are current location
        this.destination = this.path.shift();
    }
    
    /*this.label.style.top = String(0 + my_game.canvas.offsetTop + this.y - this.z - this.height/2-my_game.scene.viewport.y) + 'px';
    this.label.style.left = String(0 + my_game.canvas.offsetLeft + this.x-my_game.scene.viewport.x) + 'px';*/
    this.light.x = Math.floor(this.x+this.width/2);
    this.light.y = Math.floor(this.y-this.height/2);

    my_game.scene.center_on(this);
}
extend(glixl.Sprite, Wiz);

var Orc = function(parameters)
{
    Wiz.call(this, parameters);
}

Orc.prototype.update = function()
{    
    /*var top = my_game.canvas.offsetTop + this.y - my_game.scene.viewport.y;
    var left = my_game.canvas.offsetLeft + this.x-my_game.scene.viewport.x;
    if (top > my_game.canvas.offsetTop + my_game.canvas.clientHeight || top < my_game.canvas.offsetTop || 
        left > my_game.canvas.offsetLeft + my_game.canvas.clientWidth || left < my_game.canvas.offsetLeft)
        this.label.style.display = 'none';
    else
    {
        this.label.style.display = 'block';
        this.label.style.top = String(top) + 'px';
        this.label.style.left = String(left) + 'px';
    }*/
}
extend(Wiz, Orc);

var Rock = function(parameters)
{
    parameters.frame = 9;
    glixl.Tile.call(this, parameters);
}

Rock.prototype.use = function()
{
    console.log('Ouch!');
}
extend(glixl.Tile, Rock);

var RPG = function()
{	
    glixl.Game.call(this, {});
    
    var sprite_sheet = new glixl.SpriteSheet({context: this.context, src: 'tiles.png', frame_size: [16, 16]});
    
    var scene = new glixl.Scene({ context: this.context, width: this.width*2, height: this.height*2, sprite_sheet: sprite_sheet, tile_size: {width: 32, height: 32} });
    
    var wiz = new Wiz({frame: 41, x: 320, y:105, z:32, width:32, height:32, name: 'Player'});
    wiz.add_animation('walk_down', [50, 51, 52, 53], 120);
    wiz.set_animation('walk_down');
    scene.add_sprite(wiz);
    scene.add_light(wiz.light);
    
    var wiz = new Orc({frame: 42, x: 1200, y:666, z:32, width:32, height:32});
    scene.add_sprite(wiz);
    
    
    var MAP_SIZE = [44, 32];
    
    for (var r=0 ; r<MAP_SIZE[1] ; r++)
	{
        for (var c=0 ; c<MAP_SIZE[0] ; c++)
		{
            if (typeof map[r*MAP_SIZE[0]+c] == 'object')
            {
                for (var t=0 ; t<map[r*MAP_SIZE[0]+c].length ; t++)
                {
                    scene.add_tile(new glixl.Tile({ frame:map[r*MAP_SIZE[0]+c][t], x:c*32 , y:r*32, z:t*32, width:32, height: 32 }));
                }
            }
            else
            {
                scene.add_tile(new glixl.Tile({ frame:map[r*MAP_SIZE[0]+c], x:c*32 , y:r*32, z:0, width:32, height: 32 }));
            }
		}
	}
	
	scene.add_tile( new Rock({x:4*32 , y:6*32, z:32, width:32, height: 32 }) );
	
	scene.add_light( new glixl.Light({x: 336, y: 208, radius:130, colour: [0.9, 0.45, 0.2]}) );
	scene.add_light( new glixl.Light({x: 436, y: 408, radius:130, colour: [0.9, 0.45, 0.2]}) );
	//scene.add_light( new glixl.Light({x: 436, y: 408, radius:130, colour: [0.8, 0.8, 0.9]}) );
    
    
    
    /*for (var i=0 ; i<10 ; i++)
    {
        wiz = new glixl.Sprite({frame: 41, x: 120, y:i*32+16, z:32, width:32, height:32});
        scene.add_sprite(wiz);
    }*/

    this.set_scene(scene);
}

RPG.prototype.update = function()
{
    document.getElementById('fps').innerHTML = this.fps;
}

extend(glixl.Game, RPG);