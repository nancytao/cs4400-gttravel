$(function(){
	$('#btnSignIn').click(function(){

		$.ajax({
			url: '/sign_in',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
