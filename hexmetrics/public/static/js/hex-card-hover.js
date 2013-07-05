function done(){ //on submit function
	var s = document.createElement( 'script' );
	s.type = 'text/javascript';
	s.src = 'js/hex-card-hover.1.00.js';
	$('body').append( s );
}

function load(){ //load jQuery if it isn't already
    window.onload = function(){
        if(window.jQuery === undefined){
            var src = 'https:' == location.protocol ? 'https':'http',
                script = document.createElement('script');
            script.onload = done;
            script.src = src+'://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js';
            document.getElementsByTagName('body')[0].appendChild(script);
        }else{
            done();
        }
    }
}

if(window.readyState){ //older microsoft browsers
    window.onreadystatechange = function(){
        if(this.readyState == 'complete' || this.readyState == 'loaded'){
            load();
        }
    }
}else{ //modern browsers
    load();
}