jQuery(document).ready(function() {
	// Tabs navigation
    jQuery('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');
 
        // Show/Hide Tabs
        jQuery('.tabs ' + currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });

    // Load filtered images when available
    $('.tabs .tab-content .tab img').each(function() {
    	var $this = $(this);
    	updateImage($this, 300);
    });

});

function updateImage($imageElt, timeout)
{
    $.ajax({
        type: 'HEAD',
        url: $imageElt.attr('target'),
        error : function(){
        	$imageElt.attr('src','../static/images/spinner.gif');
            setTimeout(function(){ updateImage($imageElt, 2 * timeout); }, timeout);
        },
        success : function(data) {
            $imageElt.attr('src',$imageElt.attr('target'));
        }
    });
}
