

(function($) {
	$.fn.countTo = function(options) {
		// merge the default plugin settings with the custom options
		options = $.extend({}, $.fn.countTo.defaults, options || {});
		// how many times to update the value, and how much to increment the value on each update
		var loops = Math.ceil(options.speed / options.refreshInterval),
		increment = (options.to - options.from) / loops;

		return $(this).each(function() {
			var _this = this,
			loopCount = 0,
			value = options.from,
			interval = setInterval(updateTimer, options.refreshInterval);

			function updateTimer() {
				value += increment;
				loopCount++;
				$(_this).html(value.toFixed(options.decimals));

				if (typeof(options.onUpdate) == 'function') {
					options.onUpdate.call(_this, value);
				}

				if (loopCount >= loops) {
					clearInterval(interval);
					value = options.to;

					if (typeof(options.onComplete) == 'function') {
						options.onComplete.call(_this, value);
					}
				}
			}
		});
	};

	$.fn.countTo.defaults = {
		from: 0,				// the number the element should start at
		to: 100,				// the number the element should end at
		speed: 1000,			// how long it should take to count between the target numbers
		refreshInterval: 100,	// how often the element should be updated
		decimals: 0,			// the number of decimal places to show
		onUpdate: null,			// callback method for every time the element is updated,
		onComplete: null,		// callback method for when the element finishes updating
	};
});


function isViewed(selector) {

	var viewport = $(window),
	item = $(selector);

	var viewTop = viewport.scrollTop(),
		viewBtm = viewport.scrollTop() + viewport.height(),
		itemTop = item.offset().top,
		itemBtm = item.offset().top + item.height();

	return ((itemTop < viewBtm) && (itemTop > viewTop));
	};

	var counter = setInterval(function() {countdown()}, 500);

var countdown = function() {
	var random1 = Math.floor(Math.random()*(343-14+1)) + 14;
	var random2 = Math.floor(Math.random()*(5891-5627+1)) + 5627;
	var random3 = Math.floor(Math.random()*(686-28+1)) + 28;
	var random4 = Math.floor(Math.random()*(5627-4872+1)) + 4872;
	if(isViewed('.milestone')) {
		clearInterval(counter);
		$('.timer1').countTo({
			from: 0,
			to: 12,
			speed: 1000,
			refreshInterval: 20,
		});
		$('.timer2').countTo({
			from: 0,
			to: 93,
			speed: 1000,
			refreshInterval: 20,
		});
		$('.timer3').countTo({
			from: 0,
			to: 70,
			speed: 1000,
			refreshInterval: 20,
		});
		$('.timer4').countTo({
			from: 0,
			to: 60,
			speed: 1000,
			refreshInterval: 20,
		});
	};
}