$(document).ready(function () {
	flashed_messages();
	$('.search-overlay input[type=checkbox]').change(function () {
		return num_results();
	})
});


/*
Alerts modal
*/

function flashed_messages() {
	let messages = parseInt($("#messages p").length);
	if (messages) {
		$("#alerts").slideDown(1500);
		setTimeout(() => {
			$("#alerts").slideUp(1500);
		}, 7000);
	}
}


/* 
Search
*/

// Get number of results based on user selection
function num_results() {
	$('#tags_search_btn').html("Working...")
	// Get all checked checkboxes ("array" of elements)
	let checked = $(".form-check-input:checkbox:checked");
	// If there is no checked checkbox
	if (checked.length == 0) {
		// Empty the container
		$('#results').empty()
		// Change the header to its default value 	
		$('#num-results').html("Search")
		// Disable the btn to prevent user to submitting the form
		$('#tags_search_btn').html("Select a tag!").attr("disabled", "disabled")
		return false
	}

	// If there is at least one checked checkbox

	// Create temporary object which will hold ou
	let checkboxes = {}
	// Create a for loop to add every checked checkbox to above object
	for (let i = 0; i < checked.length; i++) {
		// {"cuisines" : "spanish"}
		checkboxes[checked[i].name] = checked[i].value
		
	}

	// Create new AJAX request to server
	$.ajax({
		type: "post",
		url: "/get_relusts",
		data: checkboxes,
		dataType: "json",
		// If success
		success: function (response) {
			// However, no results 
			if (response.doc.length == 0) {
				// Empty the container to prevent injecting the same results
				$('#results').empty()
				// Update the header 
				$('#num-results').html("Search")
				// Disable the btn to prevent user to submitting the form
				$('#tags_search_btn').html("Remove some filters!").attr("disabled", "disabled")
				return false
			}

			// At least one document match the query

			// Inject number results to header
			$('#num-results').html(response.doc.length)
			// Enable the search btn to let user to submit the form 
			$('#tags_search_btn').removeAttr("disabled").html("Search!!")
			// Empty the container to prevent injecting the same results
			$('#results').empty()
			// Loop trough the results and append each of them
			for (let i = 0; i < response.doc.length; i++) {
				// To shorten the code 
				var doc = response.doc[i]
				// Just simple example but you can go as complicated as you wish
				$('#results').append(`
					<div class="card col-md-4">
						<div>
							<a href="/recipe/5c823fa737265c3758c39907">
								<img
									class="card-img-top"
									src="${doc.image}"
									alt="${doc.title}-image"
								/>
							</a>
						</div>
						<h5 class="text-center card-title">
							${doc.title}
						</h5>
						<div class="row justify-content-center">
							<p><i class="fas fa-star fa-lg"></i>${doc.aggregateLikes}</p>
						</div>
						<hr />
					</div>
				`)
				
			}

		},

		// Iff error log XHR object
		error: function (xhr) {
			console.log(xhr)
		}
	});
}