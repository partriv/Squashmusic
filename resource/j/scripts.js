mb = {
    
    MUSIC_EVENTS_SIZE : 56,
    moreEventsLoading : false,
    moreEvents: function() {
          var min = 0; // top
          var max = ($(document).height() - $(window).height())-560; // bottom
          var curr = $(window).scrollTop();          
          
          //handle fixed nav header positioning here
          if (curr > 450){
              $('#fixednav').slideDown();
          } else {
              $('#fixednav').slideUp();
          }

          // load more events
          var vid = $('#venueselector').val();
          var cid = $('#cid').val();
          var url = '/ajax/find-events/?cid=' + cid + '&vid=' + vid;
          var end = parseInt($('#eventPg').val());
          if (curr > max) {
              end = end + mb.MUSIC_EVENTS_SIZE;
              if (mb.moreEventsLoading){
                  return;
              }
              mb.moreEventsLoading = true;
              $('#loadingMore').show();
              $.get(url + "&end=" + end, function(data){
                  $('#events').append(data);
                  $('#loadingMore').hide();
                  $('#eventPg').val(end);
                  mb.moreEventsLoading = false;
              });
              
          }
          return false;
    },
        
        
    initSearch : function(){
        $('#eventPg').val(mb.MUSIC_EVENTS_SIZE);
        window.onscroll=mb.moreEvents;
        
        $("#eventUnderlay").live('click', function(){
            window.location.hash = "event";
        });
                
        
        $('#venueselector').change(function(){
            var vid = $('#venueselector').val();
            window.location.hash ="vid=" + vid;          
        });
        $('#venueFixedSel').change(function(){
            var vid = $('#venueFixedSel').val();
            window.location.hash = "vid=" + vid;          
        });                
        
        $('#artistSearch').keyup(function(){
            var txt = $('#artistSearch').val();
            window.location.hash = "artist=" + txt;
        });
        $('#fixedArtistSearch').keyup(function(){
            var txt = $('#fixedArtistSearch').val();
            window.location.hash = "artist=" + txt;            
        });           
        
        $('#artistSearch').focus(function(){
            if ($('#artistSearch').val() == 'Artist Search'){
                $('#artistSearch').val('');
            }
        });
        $('#artistSearch').blur(function(){
            if ($('#artistSearch').val() == ''){
                $('#artistSearch').val('Artist Search');
            }
        });
        $('#fixedArtistSearch').focus(function(){
            if ($('#fixedArtistSearch').val() == 'Artist Search'){
                $('#fixedArtistSearch').val('');
            }
        });
        $('#fixedArtistSearch').blur(function(){
            if ($('#fixedArtistSearch').val() == ''){
                $('#fixedArtistSearch').val('Artist Search');
            }
        });        
        
    },
    
    loadSearch: function (vid, txt){
      var cid = $('#cid').val();
      $('#venueselector').val(vid);
      $('#venueFixedSel').val(vid);
      if (txt != "") $('#artistSearch').val(txt);
      if (txt != "") $('#fixedArtistSearch').val(txt);      
      var qs = {cid:cid, vid:vid, txt:txt};
      $.get('/ajax/find-events/', qs, function(data){
        $('#events').html(data);
      });       
      mb.hideEvent();
      return false;
    },
    
    loadEvent : function(eid){
      if (eid){
          $('#eventInfo').load('/ajax/get-event/?eid=' + eid);
          $('#eventUnderlay').show();
          $('#eventInfo').show();
      } else {
        mb.hideEvent();    
      }
      return false;
    },
    hideEvent : function(){
        $("#eventUnderlay").hide();
        $("#eventInfo").hide();
    },
    
    initContactStuff : function(){
        $('#fixedContact').click(function(){
             $(this).hide();
             $('#fixedContactForm').show("slide", { direction: "left" }, 500);
        });        
        $('#fixedContactForm .close').click(function(){      
             $('#fixedContactForm').hide("slide", { direction: "left" }, 500, function(){
                 $('#fixedContact').show();  
             });             
        });        
    },
    
    hashroutes : function(hash){
        hash = hash.replace('#', '');
        //console.log("hash route - " + hash)
        // venue id
        if (hash.indexOf('vid') > -1){
            var vid = hash.replace('vid=', '');            
            mb.loadSearch(vid, 'Artist Search');
        }
        else if (hash.indexOf('artist') > -1){
            var txt = hash.replace('artist=', '');            
            mb.loadSearch('', txt);
        }
        else if (hash.indexOf('event') > -1){
            var eid = hash.replace('event', '');            
            mb.loadEvent(eid);
        } else if (hash.indexOf('home') > -1) {
          $("#eventUnderlay").hide();
          $('#eventInfo').hide();
          mb.loadSearch('', 'Artist Search');
        }
        return false;
    }

}

$(document).ready(function(){
    mb.initContactStuff();
    mb.initSearch();
    
    // handle initial hash load here
    var hsh = window.location.hash;
    if (hsh) {
        mb.hashroutes(hsh)
    }    
})



// handle hash change events
$(window).bind('hashchange', function() {
  mb.hashroutes(window.location.hash)
});






