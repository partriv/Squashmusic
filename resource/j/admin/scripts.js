function loadEvents(){
	$('#loading').show();
	$('#events').load('/admin/ajax/find-events/?start=0&end=1000', function(){
		$('#events').fadeIn();
		$('#loading').hide();
		$('#eventPg').val(20);
	});
}

function addEventSource(){
	var name = $('#nameEventSourceTxt').val();
	var url = $('#urlEventSourceTxt').val();
	var proxy = $('#urlEventProxyTxt').val();
	return addEventSourceH(name, url, proxy);
}

function addEventSourceH(name, url, proxy) {
	if (name != ''){
		var uri = '/admin/add-event-source/?name=' + encodeURIComponent(name) + '&url=' + encodeURIComponent(url) + '&proxy=' + proxy;
		$('#addError').load(uri, function(){
			$('#sources').append('<div><a href="' + url + '">' + name + '</a> - ' + url + '</div>');
		});
	} else {
		$('#addError').html('Busted');
	}
	return false;
}

function addBulkEventSource(){	
	var strs = $('#bulkText').val().split('\n');
	var myStr;
	for (myStr in strs){
		var aStr = strs[myStr];
		if (aStr == ''){
			continue;
		}
		if (aStr.indexOf('-') == -1){
			continue;
		}		
		var aStrsGrp = aStr.split('-');
		if (aStrsGrp.length != 2){
			continue;
		}
		var name = aStrsGrp[0];
		var url = aStrsGrp[1];
		addEventSourceH(name, url);
	}
	
	return false;
}


function removeEventSource(id){
	var del = confirm("Sure you want to delete id: " + id + "?")
	if (del){
		$('#addError').load('/admin/remove-event-source/?id=' + id, function(){
			$('#source-' + id).fadeOut();
		});
	}
	return false;
}

function deleteEvent(id){
	var del = confirm("Sure you want to delete Event with id: " + id + "?")
	if (del){
		$.get('/admin/remove-event/?id=' + id, function(){
			$('#event' + id).fadeOut();
		});
	}
	return false;
}


function changeEventSourceCat(id){
	var cat = $('#catsel-' + id).val();
	$('#stat'+id).load('/admin/change-event-source-cat/?id=' + id + '&cat=' + cat, function(){
		$('#stat'+id).fadeIn();
	})
}

function changeEventItemCat(id){
	var cat = $('#catItemSel-' + id).val();
	$('#stat'+id).load('/admin/change-event-cat/?id=' + id + '&cat=' + cat, function(){
		$('#stat'+id).fadeIn();
	})
}

function changeEventCat(){
	var cat = $('#catsel').val();
	window.location='/admin/manage-events/?pg=1&cat=' + cat;
	return false;	
}

function toggleEventSourceActive(id) {	
	$('.source-active-' + id).val('Loading...');
	$('.source-active-' + id).load('/admin/toggle-event-source/?id=' + id);
	return false;
}

function findEventByName(){
	var name = $('#eventNameTxt').val();
	$('#loading').show();
	var url = '/admin/ajax/find-events/?';
	if (name != ''){
		url += 'name=' + name;
	}
	$('#events').load(url, function(){
		$('#events').fadeIn();
		$('#loading').hide();
		$('#eventPg').val(20);
	});
	
}

function toggleEventFeatured(id) {
	$('#eventFeatured-' +  id).hide();

	$('#eventFeatured-' +  id).load('/admin/ajax/toggle-event-featured/?id=' + id, function(){
		$('#eventFeatured-' +  id).show();
	});
	return false;
}


function moreAdminEvents() {
	/* not in use, can be deleted */
	  var min = 0; // top
	  var max = document.documentElement.scrollHeight - document.documentElement.clientHeight; // bottom
	  var curr = document.documentElement.scrollTop;
	  var name = $('#eventNameTxt').val();
	  var url = '/admin/ajax/find-events/?';
	  if (name != null && name != ''){
	    url += 'name=' + name;
	  }

	  var end = parseInt($('#eventPg').val());
	  if (curr == max) {
		  end = end + 20;
		  $('#loadingMore').show();
		  $.get(url + "&end=" + end, function(data){
			  $('#events').append(data);
			  $('#loadingMore').hide();
			  $('#eventPg').val(end);
		  });
		  
	  }
	  return false;
}

function addNewsSource(){
	var name = $('#nameNewsSourceTxt').val();
	var url = $('#urlNewsSourceTxt').val();
	return addNewsSourceH(name, url);
}

function addNewsSourceH(name, url) {
	if (name != '' && url != ''){
		var uri = '/admin/add-news-source/?name=' + encodeURIComponent(name) + '&url=' + encodeURIComponent(url);
		$('#addError').load(uri, function(){
			$('#sources').append('<div><a href="' + url + '">' + name + '</a> - ' + url + '</div>');
		});
	} else {
		$('#addError').html('Busted');
	}
	return false;
}

function addBulkNewsSource(){	
	var strs = $('#bulkText').val().split('\n');
	var myStr;
	for (myStr in strs){
		var aStr = strs[myStr];
		if (aStr == ''){
			continue;
		}
		if (aStr.indexOf('-') == -1){
			continue;
		}		
		var aStrsGrp = aStr.split('-');
		if (aStrsGrp.length != 2){
			continue;
		}
		var name = aStrsGrp[0];
		var url = aStrsGrp[1];
		addNewsSourceH(name, url);
	}
	
	return false;
}


function removeNewsSource(id){
	var del = confirm("Sure you want to delete id: " + id + "?")
	if (del){
		$('#addError').load('/admin/remove-news-source/?id=' + id, function(){
			$('#source-' + id).fadeOut();
		});
	}
	return false;
}

function changeNewsSourceCat(id){
	var cat = $('#catsel-' + id).val();
	$('#stat'+id).load('/admin/change-news-source-cat/?id=' + id + '&cat=' + cat, function(){
		$('#stat'+id).fadeIn();
	})
	return false;	
}

function changeNewsItemCat(){
	var cat = $('#catsel').val();
	window.location='/admin/news-items/?pg=1&cat=' + cat;
	return false;	
}

function delNewsItem(id){
	var deli = confirm("Delete this news item?");
	if (deli){
		$.get('/admin/del-news-item/?id=' + id, function(){
			$('#newsItem' + id).fadeOut();
		});
	}
	return false;	
}

function toggleFeaturedNewsItem(id){
	$('#feature-' + id).load('/admin/toggle-featured-news-item/?id=' + id, function(){
		$('#feature-' + id).fadeIn();
	});
	return false;
}

function addEtsyItem(){
	$('#loadingMore').fadeIn();
	var eid = $('#etsy_id').val();
	$.get('/admin/add-etsy-item/?id=' + eid, function(data){
		if (data.indexOf('error') == 0){
			$('#errors').html(data);
		} else {
			$('#etsy_listings').prepend(data);	
		}
		
		$('#loadingMore').fadeOut();
	});
	return false;
}

function toggleFeaturedEtsyItem(id) {	
	$('.etsy-active-' + id).val('Loading...');
	$('.etsy-active-' + id).load('/admin/toggle-featured-etsy-item/?id=' + id);
	return false;
}

function delEtsyItem(id) {	
	var conf = confirm('Delete item ' + id + '?');
	if (conf){
		$.get('/admin/del-etsy-item/?id=' + id, function(){
			$('#etsy-item-'+id).fadeOut();
		});
	}
	return false;
}



function toggleNewsSourceActive(id) {	
	$('.source-active-' + id).val('Loading...');
	$('.source-active-' + id).load('/admin/toggle-news-source/?id=' + id);
	return false;
}



function togglePhoto(id){	
	$('#photoFeature' + id).val('Loading...');
	$('#photoFeature' + id).load('/admin/toggle-featured-photo-boss-style/?id=' + id);
	return false;
}

function deletePhoto(id){	
	$.get('/admin/delete-photo/?id=' + id, function(){
		$('#photo' + id).fadeOut();
	});
	return false;
}

function addYelp(){
	var bid = $('#yelpId').val();
	$('#loadingMore').show();
	$.get('/admin/yelp/?bid=' + bid, function(data){
		$("#yelpItems").prepend(data);
		$('#yelpId').val('');
		$('#loadingMore').hide();		
	});
}

function delYelp(yid){
	var conf = confirm("Delete " + yid + "?");
	if (conf){
		$.get('/admin/yelp/?del=1&yid=' + yid, function(){
			$('#yelpItem' + yid).fadeOut();
		});
	}
}