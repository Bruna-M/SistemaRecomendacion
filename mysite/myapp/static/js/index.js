$('#form-query').submit(function (e) {
	if ($('#input-query').val()) {
		$('#spinner').show();
		$("#input-query").prop("disabled", true);
		$("#submit-button").prop("disabled", true);

		$.ajax({
	   		type: 'GET',
			url: '/get-recommendations?query=' + $('#input-query').val(),
			success: function(data) {
				if (data.error) {
					console.log('Error')
				} else {
					if ($.isEmptyObject(data.result.article_id)) {
						
						$('#table-results').hide();
					} else {
						var html = '';

						for (var index in data.result.article_id) {
							var row = '';

							row += '<tr>'
							row += '<td>' + data.result.title[index] + '</td>';
							row += '<td>' + data.result.description[index] + '</td>';
							row += '<td>' + '<a href="' + data.result.url[index] + '" target="_blank">' + data.result.url[index] + '</a>' + '</td>';
							row += '</tr>'

							html += row;
						}

						$('#table-results-body').html(html);
						$('#table-results').show();
					}
				}

				$('#spinner').hide();
				$("#input-query").prop("disabled", false);
				$("#submit-button").prop("disabled", false);
			}
	 	});
	}

    return false;
});