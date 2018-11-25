var lastWord = '';
var lastResult = {};

function processLastResult() {
	var minimumTFIDF = $('#input-minimum-tfidf').val()
	var detectedWords = [];
	
	for (var word in lastResult.weights['0']) {
		detectedWords.push(word);
	}
	
	var html = '';

	for (let i = 0; i < detectedWords.length; i++) {
		const word = detectedWords[i];
		
		html += '<h1>' + word + '</h1>';
		html += '<table>';
		html += '<thead>';
		html += '<tr>';
		html += '<th>Título</th>';
		html += '<th>URL</th>';
		html += '<th>Peso</th>';
		html += '</tr>';
		html += '</thead>';
		html += '<tbody>';

		for (var article_index in lastResult.weights) {
			const weight = lastResult.weights[article_index][word];

			if (weight > minimumTFIDF) {
				html += '<tr>';
				html += '<td>' + lastResult.articles.title[article_index] + '</td>';
				html += '<td>' + lastResult.articles.url[article_index] + '</td>';
				html += '<td>' + weight + '</td>';
				html += '</tr>';
			}
		}

		html += '</tbody>';
		html += '</table>';

		$('#section-results').html(html);
		$('#section-results').show();
	}
}

$('#form-word').submit(function (e) {
	if ($('#input-word').val()) {
		$('#spinner').show();
		$("#input-word").prop("disabled", true);
		$("#input-minimum-tfidf").prop("disabled", true);
		$("#submit-button").prop("disabled", true);

		if (lastWord == $('#input-word').val()) {
			processLastResult();

			$('#spinner').hide();
			$("#input-word").prop("disabled", false);
			$("#input-minimum-tfidf").prop("disabled", false);
			$("#submit-button").prop("disabled", false);
		} else {
			$.ajax({
				type: 'GET',
				url: '/get-report?word=' + $('#input-word').val().split(' ')[0],
				success: function(data) {
					if (data.error) {
						console.log('Error')
					} else {
						if ($.isEmptyObject(data.result.weights['0'])) {
							$('#section-results').hide();
						} else {
							lastWord = $('#input-word').val();
							lastResult = data.result;

							processLastResult();
						}
					}
	
					$('#spinner').hide();
					$("#input-word").prop("disabled", false);
					$("#input-minimum-tfidf").prop("disabled", false);
					$("#submit-button").prop("disabled", false);
				}
			});
		}
	}

    return false;
});