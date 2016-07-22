
$(function(){
	$('#login_btn').click(function(){
        $.ajax({
			url: '/login',
			type: 'POST',
        });
	});
});
