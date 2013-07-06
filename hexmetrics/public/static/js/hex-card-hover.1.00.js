$(document).ready (function () {


	$("body").append('<div style="display:none;" id="hex-cards-box"><iframe scrolling="no" style=""></iframe></div>')
	
	$('#hex-cards-box iframe').ready( function () {
		$('#hex-cards-box').css('width', '250px');
		$('#hex-cards-box').css('height', '350px');
		$('#hex-cards-box').css('margin', '0');
		$('#hex-cards-box').css('padding', '0');
		$('#hex-cards-box').css('background-color', '#000');
		
		$('#hex-cards-box iframe').css('width', '250px');
		$('#hex-cards-box iframe').css('height', '350px');
		$('#hex-cards-box iframe').css('overflow', 'hidden');
		$('#hex-cards-box iframe').css('border', 'none');
		$('#hex-cards-box iframe').css('margin', '0');
		$('#hex-cards-box iframe').css('padding', '0');
	})
	
	$("a.hex-card").each(function () {
		$(this).hover( function (e) {
			$a_ref = $(this);
			$this = $(this);
	        $.data(this, 'title', $this.attr('title'));
	        $this.removeAttr('title');
			$(document).bind('mousemove', function(e){
		    	$('#hex-cards-box').offset({left:e.pageX+20,top:e.pageY+10});
			});
			
			
			$("#hex-cards-box iframe").prop("src", 'http://hexmetrics.ni.tl/tools/cardJSFrame?url='+$a_ref.prop('href'));
			$("#hex-cards-box iframe").load ( function () {
				$("#hex-cards-box").show()
			})
					
		}, function () {
			$("#hex-cards-box").hide()
			$this = $(this);
	        $this.attr('title', $this.data('title'));
		});
	});


 
  

});