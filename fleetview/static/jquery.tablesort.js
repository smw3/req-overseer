/*
	A simple, lightweight jQuery plugin for creating sortable tables.
	https://github.com/kylefox/jquery-tablesort
	Version 0.0.11
*/

(function($) {
	$.tablesort = function ($table, settings) {
		var self = this;
		this.$table = $table;
		this.$thead = this.$table.find('thead');
		this.settings = $.extend({}, $.tablesort.defaults, settings);
		this.$sortCells = this.$thead.length > 0 ? this.$thead.find('th:not(.no-sort)') : this.$table.find('th:not(.no-sort)');
		this.$sortCells.on('click.tablesort', function() {
			self.sort($(this));
		});
		this.index = null;
		this.$th = null;
	};

	$.tablesort.prototype = {

		sort: function(th) {
			var start = new Date(),
				self = this,
				table = this.$table,
				thead = this.$table.find('thead'),
				sortCells = this.$thead.length > 0 ? this.$thead.find('th:not(.no-sort)') : this.$table.find('th:not(.no-sort)'),
				rowsContainer = table.find('tbody').length > 0 ? table.find('tbody') : table,
				rows = rowsContainer.find('tr').has('td, th'),
				cells = rows.find(':nth-child(' + (th.index() + 1) + ')').filter('td, th'),
				sortBy = th.data().sortBy,
				sortedMap = [];

			var unsortedValues = cells.map(function(idx, cell) {
				if (sortBy)
					return (typeof sortBy === 'function') ? sortBy($(th), $(cell), self) : sortBy;
				return ($(this).data().sortValue != null ? $(this).data().sortValue : $(this).text());
			});
			if (unsortedValues.length === 0) return;

			var direction = 'asc';
			if (th.hasClass("sort-asc")) {
				th.removeClass("sort-asc").addClass("sort-desc").removeClass("sort-none");
				direction = 'desc';
				console.log(sortCells);
				$.each(sortCells, function( index, value ) {
					value.removeClass("sort-asc").removeClass("sort-desc").addClass("sort-none");
					value.find( "i" ).removeClass("fa-sort-up").removeClass("fa-sort-down").addClass("fa-sort");
				});
				th.find( "i" ).removeClass("fa-sort-up").addClass("fa-sort-down").removeClass("fa-sort");
			} else if (th.hasClass("sort-desc")) {
				th.removeClass("sort-asc").removeClass("sort-desc").addClass("sort-none");
				th.find( "i" ).removeClass("fa-sort-up").removeClass("fa-sort-down").addClass("fa-sort");
				return;
			} else {
				th.addClass("sort-asc").removeClass("sort-desc").removeClass("sort-none");
				direction = 'asc';
				console.log(sortCells);
				$.each(sortCells, function( index, value ) {
					value.removeClass("sort-asc").removeClass("sort-desc").addClass("sort-none");
					value.find( "i" ).removeClass("fa-sort-up").removeClass("fa-sort-down").addClass("fa-sort");
				});
				th.find( "i" ).addClass("fa-sort-up").removeClass("fa-sort-down").removeClass("fa-sort");
			}

			self.$table.trigger('tablesort:start', [self]);
			self.log("Sorting by " + this.index + ' ' + this.direction);

			// Try to force a browser redraw
			self.$table.css("display");
			// Run sorting asynchronously on a timeout to force browser redraw after
			// `tablesort:start` callback. Also avoids locking up the browser too much.
			setTimeout(function() {
				self.$sortCells.removeClass(self.settings.asc + ' ' + self.settings.desc);
				for (var i = 0, length = unsortedValues.length; i < length; i++)
				{
					sortedMap.push({
						index: i,
						cell: cells[i],
						row: rows[i],
						value: unsortedValues[i]
					});
				}

				sortedMap.sort(function(a, b) {
					return self.settings.compare(a.value, b.value) * direction;
				});

				$.each(sortedMap, function(i, entry) {
					rowsContainer.append(entry.row);
				});

				th.addClass(self.settings[self.direction]);

				self.log('Sort finished in ' + ((new Date()).getTime() - start.getTime()) + 'ms');
				self.$table.trigger('tablesort:complete', [self]);
				//Try to force a browser redraw
				self.$table.css("display");
			}, unsortedValues.length > 2000 ? 200 : 10);
		},

		log: function(msg) {
			if(($.tablesort.DEBUG || this.settings.debug) && console && console.log) {
				console.log('[tablesort] ' + msg);
			}
		},

		destroy: function() {
			this.$sortCells.off('click.tablesort');
			this.$table.data('tablesort', null);
			return null;
		}

	};

	$.tablesort.DEBUG = false;

	$.tablesort.defaults = {
		debug: $.tablesort.DEBUG,
		asc: 'sorted ascending',
		desc: 'sorted descending',
		compare: function(a, b) {
			if (a > b) {
				return 1;
			} else if (a < b) {
				return -1;
			} else {
				return 0;
			}
		}
	};

	$.fn.tablesort = function(settings) {
		var table, sortable, previous;
		return this.each(function() {
			table = $(this);
			previous = table.data('tablesort');
			if(previous) {
				previous.destroy();
			}
			table.data('tablesort', new $.tablesort(table, settings));
		});
	};

})(window.Zepto || window.jQuery);
