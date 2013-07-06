$(document).ready (function () {

	$("body").append('<div style="display:none;" id="hex-cards-box"><iframe scrolling="no" style=""></iframe></div>')

	var mouseX;
	var mouseY;
	$(document).mousemove( function(e) {
   		mouseX = e.pageX; 
   		mouseY = e.pageY;
   		$('#hex-cards-box').offset({left:e.mouseX+20,top:e.pageY+10});
		if($should_show_hex == false) $("#hex-cards-box").hide();
	}); 
	
	$('#hex-cards-box iframe').ready( function () {
		$('#hex-cards-box').css('width', '251px');
		$('#hex-cards-box').css('height', '386px');
		$('#hex-cards-box').css('margin', '0');
		$('#hex-cards-box').css('padding', '0');
		
		$('#hex-cards-box iframe').css('width', '250px');
		$('#hex-cards-box iframe').css('height', '385px');
		$('#hex-cards-box iframe').css('overflow', 'hidden');
		$('#hex-cards-box iframe').css('border', 'none');
		$('#hex-cards-box iframe').css('margin', '0');
		$('#hex-cards-box iframe').css('padding', '0');
	})
	
	$should_show_hex = true;
	
	$("a.hex-card").each(function () {
		$(this).hover( function (h) {
			$a_ref = $(this);
			$this = $(this);
	        $.data(this, 'title', $this.attr('title'));
	        $this.removeAttr('title');
			
			$should_show_hex = true;
			$('#hex-cards-box').offset({left:h.pageX+20,top:h.pageY+10});
			$("#hex-cards-box iframe").prop("src", 'http://hexmetrics.ni.tl/tools/cardJSFrame?url='+$a_ref.prop('href'));
			$("#hex-cards-box iframe").load ( function () {
				if($should_show_hex == true) $("#hex-cards-box").show();
				$('#hex-cards-box').offset({left:mouseX+20,top:mouseY+10});
			})
					
		}, function () {
			$should_show_hex = false;
			$("#hex-cards-box").hide()
			$this = $(this);
	        $this.attr('title', $this.data('title'));
		});
	});


 
  

});