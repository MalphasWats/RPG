/* glixl2 */
var glixl = (function(glixl)
{
    glixl.Game = function Game(parameters)
    {
        this.canvas = document.getElementsByTagName('canvas')[0];
        if (!this.canvas)
            throw new Error("*** ERROR: Could not find canvas element");
        
        this.width = this.canvas.clientWidth
        this.height = this.canvas.clientHeight
            
        this.context = this.canvas.getContext("webgl");
        if (!glixl.context)
        {
            this.context = this.canvas.getContext("experimental-webgl");
            if (!this.context)
                throw new Error("*** ERROR: Unable to create webgl context");
        }
        
        var vertex_shader_source = parameters.vertex_shader_source || `
            attribute vec3 a_position;
            uniform mat4 viewport_matrix;
            uniform mat4 projection_matrix;
            
            attribute vec2 a_texCoords;
            varying vec2 v_texCoords;
            
            void main()
            {
                gl_Position = projection_matrix * viewport_matrix  * vec4(a_position, 1);
                //gl_Position = projection_matrix * vec4(a_position, 1);
                //gl_Position = viewport_matrix * vec4(a_position, 1);
                v_texCoords = a_texCoords;
            }
        `;
        
        var fragment_shader_source = parameters.fragment_shader_source || `
            precision mediump float;
            uniform sampler2D u_image;
            varying vec2 v_texCoords;
            
            void main() 
            { 
                vec4 frag_color = texture2D(u_image, v_texCoords);
                if (frag_color.a < 1.0)
                    discard;
                    
                gl_FragColor = frag_color;
            }
        `;
        
        this.shader_program = this.build_shader_program(vertex_shader_source, fragment_shader_source);
        this.context.useProgram(this.shader_program);
        
        this.context.program = this.shader_program;
        
        this.context.enable ( this.context.DEPTH_TEST );
        
        /*window.addEventListener("keydown", this.handle_key_down);
        window.addEventListener("keyup", this.handle_key_up);
        
        this.keys = {};
        
        this.mouse_x = 0;
        this.mouse_y = 0;
        this.mouse_down = false;
        
        window.addEventListener("mousemove", this.save_mouse_position);
        this.canvas.addEventListener("mousedown", this.handle_mouse_down, false);
        this.canvas.addEventListener("mouseup", this.handle_mouse_up, false);
        this.canvas.addEventListener("touchstart", this.handle_mouse_down, false);
        this.canvas.addEventListener("touchend", this.handle_mouse_up, false);*/
        
        this.canvas.addEventListener("mouseup", this.handle_mouse_up.bind(this), false);
        
        this.event_queue = [];
        
        /* TODO: Create a 'loading' scene */

        this.prevTS = 0;
        this.fps_stream = [];
        this.fps = 0;
    }
    
    glixl.Game.prototype.build_shader_program = function(vertex_shader_source, fragment_shader_source)
    {
        var vertex_shader = this.context.createShader(this.context.VERTEX_SHADER);
        this.context.shaderSource(vertex_shader, vertex_shader_source);
        this.context.compileShader(vertex_shader);

        var compiled = this.context.getShaderParameter(vertex_shader, this.context.COMPILE_STATUS);
        if (!compiled) 
        {
            this.context.deleteShader(vertex_shader);
            var lastError = this.context.getShaderInfoLog(vertex_shader);
            throw new Error("*** Error: Could not compile shader '" + vertex_shader + "' : " + lastError);
        }
        
        var fragment_shader = this.context.createShader(this.context.FRAGMENT_SHADER);
        this.context.shaderSource(fragment_shader, fragment_shader_source);
        this.context.compileShader(fragment_shader);
        
        var compiled = this.context.getShaderParameter(fragment_shader, this.context.COMPILE_STATUS);
        if (!compiled) 
        {
            this.context.deleteShader(fragment_shader);
            var lastError = this.context.getShaderInfoLog(fragment_shader);
            throw new Error("*** Error: Could not compile shader '" + fragment_shader + "' : " + lastError);
        }
        
        var program = this.context.createProgram();
        this.context.attachShader(program, vertex_shader);
        this.context.attachShader(program, fragment_shader);
        
        this.context.linkProgram(program);
        var linked = this.context.getProgramParameter(program, this.context.LINK_STATUS);
        if (!linked) 
        {
            // something went wrong with the link
            this.context.deleteProgram(program);
            var lastError = this.context.getProgramInfoLog(program);
            throw new Error("*** Error: Could not link program: " + lastError);
        }
        
        return program;
    }
    
    glixl.Game.prototype.set_scene = function(scene)
    {
        this.scene = scene;
        this.scene.initialise_viewport({x: 0, y:0, width:this.width, height:this.height});
        
        this.scene.sprite_sheet.bind();
    }
    
    glixl.Game.prototype.start = function()
    {
        console.log('Game Started!');
        /*this.app_loop = function(ts)
        {
            //glixl.update_fps(ts);
            
            //glixl.update();
            //glixl.app.update();
            console.log(this);
            this.scene.draw();
            window.requestAnimationFrame(this.app_loop);
        }*/
        
        window.requestAnimationFrame(this.game_loop.bind(this));
    }
    
    glixl.Game.prototype.game_loop = function(ts)
    {
        this.update();
        this.scene.update();
        this.scene.draw();
        
        for (var i=0 ; i<this.event_queue.length ; i++)
            this.event_queue[i].use();
            
        this.event_queue = [];
        
        var delta = ts - this.prevTS;
        this.prevTS = ts;
        
        this.fps_stream.unshift(1000 / delta);
        this.fps_stream = this.fps_stream.slice(0, 20);
        var sum = 0;
        for (var i=0 ; i<20 ; i++)
            sum += this.fps_stream[i];
            
        this.fps = Math.round(sum/20);
        
        window.requestAnimationFrame(this.game_loop.bind(this));
    }
    
    glixl.Game.prototype.update = function()
    {
        
    }
    
    glixl.Game.prototype.draw = function()
    {
        
    }
    
    glixl.Game.prototype.handle_mouse_up = function(e)
    {
        var mouse_x = (e.pageX - this.canvas.offsetLeft) + this.scene.viewport.x;
        var mouse_y = (e.pageY - this.canvas.offsetTop) + this.scene.viewport.y;
        
        var item = this.scene.get_topmost_item(mouse_x, mouse_y);
        this.event_queue.push(item);
    }
        
    return glixl;
    
})(glixl || {});