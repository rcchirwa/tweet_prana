	$(function(){


		var tweet_engine = {

			//data structure containing the business rules for branding
			b_rules: {

				buyer: {
					pattern: /consumer/gi,
					 pc_term: "Buyer"
					},
		 
				maker: {
					//pattern: /(maker|subscriber)/gi,
					pattern: /(subscriber)/gi,
					pc_term: "Maker"
				},

				dashboard: {
					pattern: /(admin|back_*-*end)/gi,
					pc_term: "Dashboard"
				},

				buyer_dashboard: 
				{
					pattern: /conback/gi,
					pc_term: "Buyer Dashboard"
				},

				maker_dashboard: 
				{
					pattern: /subb*ack/gi,
					pc_term: "Maker Dashboard"
				}
			},

			//patterns to search for dirty words i.e. list of words and ALL CAPS 
			dirty_patterns: [/(big box|generic|commodity|mass market)/gi, /[A-Z]{2,}/g],

			//this is where a list of dirty words are found
			dirty_words_found:  [],
			
			//two key-values hold the status of the tweet after it has been analyzed
			is_branding_clean: false,

			is_tweet_dirty: false, 

			//Strings to hold the original and the brand corrected tweets as well as highlighted versions 
			brand_corrected_tweet: "", 

			original_tweet: "", 
			
			//the two string below are used for modals
			highlighted_brand_corrected_tweet: "", 
			
			highlighted_original_tweet: "", 


			//looks at the tweet and processes to verify the branding			
			branding_filter: function (){

				//initialize tweets to mirror the original tweets
				//create a copt of the original string that can be modified
				var tweet_string = this.original_tweet;


				this.highlighted_original_tweet = tweet_string;
				
				this.highlighted_brand_corrected_tweet = tweet_string;

				//initiate a variable for the matches found 
				var matches;
	


				//iterate through the branding rules defined above. 
				for (var key in this.b_rules) {

	 			 	if (this.b_rules.hasOwnProperty(key)) {
    					//retrieve pattern
    					obj_pattern = this.b_rules[key]['pattern'];

    					//corresponding correct term
    					obj_pc = this.b_rules[key]['pc_term'];

    					//search the tweet for the current pettern match
    					matches = tweet_string.match(obj_pattern);

    					//if matched found
    					if (matches)
    					{
    						//go through the found  matches and replace them with highlighted spans to highlight them
    						for(i=0;i<matches.length;i++)
    						{
    							this.highlighted_original_tweet = this.highlighted_original_tweet.replace(matches[i],"<span class=\"text-error\">" + matches[i] + "</span>");
    						}
    					}

    					//go through the original tweet and replace the tweet string because this will  need to be corrected to proceed to the next correction
						tweet_string  = tweet_string.replace(obj_pattern,obj_pc);

						//Go thorugh the string holding the brand corrected tweet and highlight the words that were corrected 
						this.highlighted_brand_corrected_tweet = this.highlighted_brand_corrected_tweet.replace(obj_pattern,"<span class=\"text-success\">" + obj_pc + "</span>");

  					}
				}

				//check to see if the tweet was altered and if so the branding was clean
				this.is_branding_clean = (tweet_string==this.original_tweet);
				
				//the plain brand corrected tweet is equivelent to the tweet_string that was modified
				this.brand_corrected_tweet = tweet_string;
			},	


			isDirty: function(){
				var dirty = false;
				var matches = []

				//create a copt of the original string that can be modified
				var tweet_string = this.original_tweet;

				//lets iterate through the patterns 
				for (i=0;i<this.dirty_patterns.length;i++){

					//create the regular expresion pattern 
					var patt1 = new RegExp(this.dirty_patterns[i]);

					//Check to see if the tweet string has dirty words
					pattern_test_result = patt1.test(tweet_string);

					//if pattern found
					if (pattern_test_result)
					{
						//set dirty to true
						dirty = pattern_test_result;

						//add the found dirty words to the structure holding the matches
						matches = matches.concat(tweet_string.match(patt1));
					}
				}

				//set the object variable
				this.dirty_words_found = matches;
				this.is_tweet_dirty = dirty;
			},
			//this instantiate the object
			instantiate: function(tweet_string)
			{
				this.original_tweet = tweet_string
				this.isDirty();
				this.branding_filter();
			}

		}



		//The behavior below is is responsible for processing the modal that alerts the user about branding violations
		$('#accept_changes').click(function(){
			$('#tweet_text').val(tweet_engine.brand_corrected_tweet);
			$('#brandingModal').modal('hide');
			$('#brand_modal_correction').html("");
			$('#brand_modal_original').html("");
		});


		//this handles the tweet submission. 
		$('#tweet_form').submit(function(e){
			e.preventDefault();
			e.stopPropagation();
			$(this).prop('disabled', true);

			//get what is in the textarea
			var tweet_string = $('#tweet_text').val();

			//I like to to see the best in people so lets assume clean
			var status = "clean";

			//instantiate the tweet engine
			tweet_engine.instantiate(tweet_string);

			//check to see if the branding was violated
	  		if (!tweet_engine.is_branding_clean)
	  		{
	  			$('#brand_modal_correction').html(tweet_engine.highlighted_brand_corrected_tweet);
	  			$('#brand_modal_original').html(tweet_engine.highlighted_original_tweet);
	  			$('#brandingModal').modal('show');
	  			return false;
	  		}
	  		//check to see if the branding is dirty
	  		else if (tweet_engine.is_tweet_dirty)
	  		{
	  			var status = "dirty";
				//return false;
	  		}


	  		var uri = $('form').attr('action');
	  		var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

	  		//data to send in json object to the server
			formData = {csrfmiddlewaretoken: csrfToken, tweet: tweet_string, status: status};

			$.ajax({
        		type: "POST",
        		url: uri,
        		data: formData,
        		//for showing user after tweet completion either good or bad
        		after_tweet_modal: function(header,body,isDirty){
        				$('#tweet_result_modal_header').html(header);
	  					$('#tweet_result_modal_body').html(body);

	  					if (isDirty)
	  					{
	  						$('#tweet_result_modal_body').addClass('text-error');
		  					$('#tweet_result_modal').modal('show');
		  				}	  					
		  				else
		  				{
		  					$('#tweet_result_modal_body').removeClass('text-error');
		  					window.setTimeout($('#tweet_result_modal').modal('show'), 2000);
		  				}
	  					
        		},
        		success: function (data) {
        			//if the tweet was dirty flash the message

        			if (tweet_engine.is_tweet_dirty)
        			{
	        			var shame_text = "Shame for tweeting the following dirty words: " + tweet_engine.dirty_words_found.join(',');
        				$("#shameOnYou").html(shame_text);
        				$('#dirtyWordBox').removeClass("hidden_elem");
        				this.after_tweet_modal('SHAME ON YOU',shame_text,tweet_engine.is_tweet_dirty);
        				$('#tweet_result_modal_body').addClass('text-error');
        			}
        			else
        			{
        				this.after_tweet_modal('Success',data.tweet_html,tweet_engine.is_tweet_dirty);
	  				}

	  				$('#tweet_text').val('');
        			$(this).prop('disabled', false);
        			$('#word-counter').text(140)
        		},
        		error: function(jqXHR, exception) {
            		console.log("jqXHR.status: " + jqXHR.status);
                	console.log("exception: " + exception);
        		}  
    		});  
		});


		//this is a global variable
		var toggle_warning = true;

		function tweet_keylogger(inhere,toggler){

			//don't know if this verios of javascript has trim()
			var trimmed_str = inhere.val().replace(/^\s+|\s+$/g, '');

			//check the trimmed string length 
			var str_len = trimmed_str.length;

			//update the counter to reflect how many characters can still be displayed 
			$('#word-counter').text(140-str_len);

			//if the characters are more then 140
			if (str_len > 140){
				//if toggler is true then action needs to be performed
				if (toggler==true){ 
					toggler = false;//reset toggler state
					$('#word-counter').addClass('text-error lead');
					$('#tweet_btn').prop('disabled', true).removeClass('btn-primary');
				}
			}
			else if (str_len > 0)
			{
				if (toggler==false){ 
					toggler = true;//reset toggler stat
					$('#word-counter').removeClass('text-error lead');
					$('#tweet_btn').prop('disabled', false).addClass('btn-primary');	
				}
			}
			else if (str_len == 0)
			{
					toggler = false;
					$('#tweet_btn').prop('disabled', true).removeClass('btn-primary');
			}

			//toggler is only true between 1 and 140
			return toggler
		}

		//This handles any modification or change in the text area
		$('#tweet_text').on('keyup keypress blur change', function(e){
			toggle_warning = tweet_keylogger($(this),toggle_warning);
		});


		//this handle closing the shame on you message dispalayed to the user when the have submitted tweet with dirty word
		$('#closeDirtyWord').click(function(){
									$('#dirtyWordBox').addClass("hidden_elem");
									$("#shameOnYou").html("");
								})



	})/*end jquery*/