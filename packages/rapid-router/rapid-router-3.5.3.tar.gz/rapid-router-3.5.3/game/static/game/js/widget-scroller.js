/*! Widget: scroller - updated 5/17/2015 (v2.22.0) *//*
 Copyright (C) 2011 T. Connell & Associates, Inc.

 Dual-licensed under the MIT and GPL licenses

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
 LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
 NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE	FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 Resizable scroller widget for the jQuery tablesorter plugin

 Version 2.0 - modified by Rob Garrison 4/12/2013;
 updated 3/5/2015 (v2.22.2) with lots of help from TheSin-
 Requires jQuery v1.7+
 Requires the tablesorter plugin, v2.8+, available at http://mottie.github.com/tablesorter/docs/

 Usage:
 $(function() {
 $('table.tablesorter').tablesorter({
 widgets: ['zebra', 'scroller'],
 widgetOptions : {
 scroller_height       : 300,  // height of scroll window
 scroller_jumpToHeader : true, // header snap to browser top when scrolling the tbody
 scroller_upAfterSort  : true, // scroll tbody to top after sorting
 scroller_fixedColumns : 0     // set number of fixed columns
 }
 });
 });

 Website: www.tconnell.com
 */
/*jshint browser:true, jquery:true, unused:false */
;( function( $, window ) {
    'use strict';

    var ts = $.tablesorter,
        tscss = ts.css;

    $.extend( ts.css, {
        scrollerWrap        : 'tablesorter-scroller',
        scrollerHeader      : 'tablesorter-scroller-header',
        scrollerTable       : 'tablesorter-scroller-table',
        scrollerFooter      : 'tablesorter-scroller-footer',
        scrollerFixed       : 'tablesorter-scroller-fixed',
        scrollerFixedPanel  : 'tablesorter-scroller-fixed-panel',
        scrollerHasFix      : 'tablesorter-scroller-has-fixed-columns',
        scrollerHideColumn  : 'tablesorter-scroller-hidden-column',
        scrollerHideElement : 'tablesorter-scroller-hidden',
        scrollerSpacerRow   : 'tablesorter-scroller-spacer',
        scrollerBarSpacer   : 'tablesorter-scroller-bar-spacer',
        scrollerAddedHeight : 'tablesorter-scroller-added-height',
        scrollerHack        : 'tablesorter-scroller-scrollbar-hack',
        scrollerReset       : 'tablesorter-scroller-reset',
        // class name on table cannot start with 'tablesorter-' or the
        // suffix "scroller-rtl" will match as a theme name
        scrollerRtl         : 'ts-scroller-rtl'
    });

    ts.addWidget({
        id : 'scroller',
        priority : 60, // run after the filter widget
        options : {
            scroller_height : 300,
            // pop table header into view while scrolling up the page
            scroller_jumpToHeader : true,
            // scroll tbody to top after sorting
            scroller_upAfterSort : true,
            // set number of fixed columns
            scroller_fixedColumns : 0,
            // add hover highlighting to the fixed column (disable if it causes slowing)
            scroller_rowHighlight : 'hover',
            // add a fixed column overlay for styling
            scroller_addFixedOverlay : false,
            // In tablesorter v2.19.0 the scroll bar width is auto-detected
            // add a value here to override the auto-detected setting
            scroller_barWidth : null
        },
        format : function( table, c, wo ) {
            if ( !c.isScrolling ) {
                // initialize here instead of in widget init to give the
                // filter widget time to finish building the filter row
                ts.scroller.setup( c, wo );
            }
        },
        remove : function( table, c, wo ) {
            ts.scroller.remove( c, wo );
        }
    });

    /* Add window resizeEnd event */
    ts.window_resize = function() {
        if ( ts.timer_resize ) {
            clearTimeout( ts.timer_resize );
        }
        ts.timer_resize = setTimeout( function() {
            $( window ).trigger( 'resizeEnd' );
        }, 250 );
    };

// Add extra scroller css
    $( function() {
        var style = '<style>' +
                /* reset width to get accurate measurements after window resize */
            '.' + tscss.scrollerReset + ' { width: auto !important; min-width: auto !important; max-width: auto !important; }' +
                /* overall wrapper & table section wrappers */
            '.' + tscss.scrollerWrap + ' { position: relative; overflow: hidden; }' +
                /* add border-box sizing to all scroller widget tables; see #135 */
            '.' + tscss.scrollerWrap + ' * { box-sizing: border-box; }' +
            '.' + tscss.scrollerHeader + ', .' + tscss.scrollerFooter + ' { position: relative; overflow: hidden; }' +
            '.' + tscss.scrollerHeader + ' table.' + tscss.table + ' { margin-bottom: 0; }' +
                /* always leave the scroll bar visible for tbody, or table overflows into the scrollbar
                 when height < max height (filtering) */
            '.' + tscss.scrollerTable + ' { position: relative; overflow: auto; }' +
            '.' + tscss.scrollerTable + ' table.' + tscss.table +
            ' { border-top: 0; margin-top: 0; margin-bottom: 0; overflow: hidden; }' +
                /* hide footer in original table */
            '.' + tscss.scrollerTable + ' tfoot, .' + tscss.scrollerHideElement + ', .' + tscss.scrollerHideColumn +
            ' { display: none; }' +

            /*** fixed column ***/
                /* disable pointer-events on fixed column wrapper or the user can't interact with the horizontal scrollbar */
            '.' + tscss.scrollerFixed + ', .' + tscss.scrollerFixed + ' .' + tscss.scrollerFixedPanel +
            ' { pointer-events: none; }' +
                /* enable pointer-events for fixed column children; see #135 & #878 */
            '.' + tscss.scrollerFixed + ' > div { pointer-events: all; }' +
            '.' + tscss.scrollerWrap + ' .' + tscss.scrollerFixed + ' { position: absolute; top: 0; z-index: 1; left: 0 } ' +
            '.' + tscss.scrollerWrap + ' .' + tscss.scrollerFixed + '.' + tscss.scrollerRtl + ' { left: auto; right: 0 } ' +
                /* add horizontal scroll bar; set to "auto", see #135 */
            '.' + tscss.scrollerWrap + '.' + tscss.scrollerHasFix + ' > .' + tscss.scrollerTable + ' { overflow: auto; }' +
                /* need to position the tbody & tfoot absolutely to hide the scrollbar & move the footer
                 below the horizontal scrollbar */
            '.' + tscss.scrollerFixed + ' .' + tscss.scrollerFooter + ' { position: absolute; bottom: 0; }' +
                /* hide fixed tbody scrollbar - see http://goo.gl/VsLe6n */
            '.' + tscss.scrollerFixed + ' .' + tscss.scrollerTable +
            ' { position: relative; left: 0; overflow: hidden; -ms-overflow-style: none; }' +
            '.' + tscss.scrollerFixed + ' .' + tscss.scrollerTable + '::-webkit-scrollbar { display: none; }' +
            /*** fixed column panel ***/
            '.' + tscss.scrollerWrap + ' .' + tscss.scrollerFixedPanel +
            ' { position: absolute; top: 0; bottom: 0; z-index: 2; left: 0; right: 0; } ' +
            '</style>';
        $( style ).appendTo( 'body' );
    });

    ts.scroller = {

        // Ugh.. Firefox misbehaves, so it needs to be detected
        isFirefox : navigator.userAgent.toLowerCase().indexOf( 'firefox' ) > -1,
        // old IE needs a wrap to hide the fixed column scrollbar; http://stackoverflow.com/a/24408672/145346
        isOldIE : document.all && !window.atob,
        // http://stackoverflow.com/questions/7944460/detect-safari-browser - needed to position scrolling body
        // when the table is set up in RTL direction
        isSafari : navigator.userAgent.toLowerCase().indexOf( 'safari' ) > -1 &&
        navigator.userAgent.toLowerCase().indexOf( 'chrome' ) === -1,

        hasScrollBar : function( $target, checkWidth ) {
            if ( checkWidth ) {
                return $target.get(0).scrollWidth > $target.width();
            } else {
                return $target.get(0).scrollHeight > $target.height();
            }
        },

        setWidth : function( $el, width ) {
            $el.css({
                'width' : width,
                'min-width' : width,
                'max-width' : width
            });
        },

        // modified from http://davidwalsh.name/detect-scrollbar-width
        getBarWidth : function() {
            var $div = $( '<div>' ).css({
                    'position' : 'absolute',
                    'top' : '-9999px',
                    'left' : 0,
                    'width' : '100px',
                    'height' : '100px',
                    'overflow' : 'scroll',
                    'visibility' : 'hidden'
                }).appendTo( 'body' ),
                div = $div[0],
                barWidth = div.offsetWidth - div.clientWidth;
            $div.remove();
            return barWidth;
        },

        setup : function( c, wo ) {
            var maxHt, tbHt, $hdr, $t, $hCells, $fCells, $tableWrap, tmp,
                $win = $( window ),
                namespace = c.namespace + 'tsscroller',
                $foot = $(),
            // c.namespace contains a unique tablesorter ID, per table
                id = c.namespace.slice( 1 ) + 'tsscroller',
                $table = c.$table;

            // set scrollbar width & allow setting width to zero
            wo.scroller_barSetWidth = wo.scroller_barWidth !== null ?
                wo.scroller_barWidth :
                ( ts.scroller.getBarWidth() || 15 );

            maxHt = wo.scroller_height || 300;
            // sum all tbody heights
            tbHt = 0;
            $table.children( 'tbody' ).map( function() {
                tbHt += $( this ).outerHeight();
            });

            $hdr = $( '<table class="' + $table.attr( 'class' ) + '" cellpadding=0 cellspacing=0>' +
            $table.children( 'thead' )[ 0 ].outerHTML + '</table>' );
            wo.scroller_$header = $hdr.addClass( c.namespace.slice( 1 ) + '_extra_table' );

            $t = $table.children( 'tfoot' );
            if ( $t.length ) {
                $foot = $( '<table class="' + $table.attr( 'class' ) +
                '" cellpadding=0 cellspacing=0 style="margin-top:0"></table>' )
                    .addClass( c.namespace.slice( 1 ) + '_extra_table' )
                    // maintain any bindings on the tfoot cells
                    .append( $t.clone( true ) )
                    .wrap( '<div class="' + tscss.scrollerFooter + '"/>' );
                $fCells = $foot.children( 'tfoot' ).eq( 0 ).children( 'tr' ).children();
            }
            wo.scroller_$footer = $foot;

            $table
                .wrap( '<div id="' + id + '" class="' + tscss.scrollerWrap + '" />' )
                .before( $hdr )
                // shrink filter row but don't completely hide it because the inputs/selectors may distort the columns
                .find( '.' + tscss.filterRow )
                .addClass( tscss.filterRowHide );

            wo.scroller_$container = $table.parent();

            if ( $foot.length ) {
                // $foot.parent() to include <div> wrapper
                $table.after( $foot.parent() );
            }

            $hCells = $hdr
                .wrap( '<div class="' + tscss.scrollerHeader + '" />' )
                .find( '.' + tscss.header );

            // use max-height, so the height resizes dynamically while filtering
            $table.wrap( '<div class="' + tscss.scrollerTable + '" style="max-height:' + maxHt + 'px;" />' );
            $tableWrap = $table.parent();

            // make scroller header sortable
            ts.bindEvents( c.table, $hCells );

            // look for filter widget
            if ( $table.hasClass( 'hasFilters' ) ) {
                ts.filter.bindSearch( $table, $hdr.find( '.' + tscss.filter ) );
            }

            $table
                .find( 'thead' )
                .addClass( tscss.scrollerHideElement );

            tbHt = $tableWrap.parent().height();

            // The header will always jump into view if scrolling the table body
            $tableWrap
                .off( 'scroll' + namespace )
                .on( 'scroll' + namespace, function() {
                    if ( wo.scroller_jumpToHeader ) {
                        var pos = $win.scrollTop() - $hdr.offset().top;
                        if ( $( this ).scrollTop() !== 0 && pos < tbHt && pos > 0 ) {
                            $win.scrollTop( $hdr.offset().top );
                        }
                    }
                    $hdr
                        .parent()
                        .add( $foot.parent() )
                        .scrollLeft( $( this ).scrollLeft() );
                });

            // Sorting, so scroll to top
            tmp = 'sortEnd setFixedColumnSize updateComplete pagerComplete pagerInitialized columnUpdate '
                .split( ' ' )
                .join( namespace + ' ' );
            $table
                .off( tmp )
                .on( 'sortEnd' + namespace, function() {
                    if ( wo.scroller_upAfterSort ) {
                        $table.parent().animate({
                            scrollTop : 0
                        }, 'fast' );
                    }
                })
                .on( 'setFixedColumnSize' + namespace, function( event, size ) {
                    var $wrap = wo.scroller_$container;
                    if ( typeof size !== 'undefined' && !isNaN( size ) ) {
                        wo.scroller_fixedColumns = parseInt( size, 10 );
                    }
                    // remove fixed columns
                    ts.scroller.removeFixed( c, wo );
                    size = wo.scroller_fixedColumns;
                    if ( size > 0 && size < c.columns - 1 ) {
                        ts.scroller.updateFixed( c, wo );
                    } else if ( $wrap.hasClass( tscss.scrollerHasFix ) ) {
                        $wrap.removeClass( tscss.scrollerHasFix );
                        // resize needed to make tables full width
                        ts.scroller.resize( c, wo );
                    }
                })
                .on( 'updateComplete pagerComplete pagerInitialized columnUpdate '
                    .split( ' ' ).join( namespace + ' ' ), function() {
                    // adjust column sizes after an update
                    ts.scroller.resize( c, wo );
                });

            // Setup window.resizeEnd event
            $win
                .off( 'resize resizeEnd '.split( ' ' ).join( namespace + ' ' ) )
                .on( 'resize' + namespace, ts.window_resize )
                .on( 'resizeEnd' + namespace, function() {
                    // IE calls resize when you modify content, so we have to unbind the resize event
                    // so we don't end up with an infinite loop. we can rebind after we're done.
                    $win.off( 'resize' + namespace, ts.window_resize );
                    ts.scroller.resize( c, wo );
                    $win.on( 'resize' + namespace, ts.window_resize );
                    $tableWrap.trigger( 'scroll' + namespace );
                });

            // initialization flag
            c.isScrolling = true;

            ts.scroller.updateFixed( c, wo );

        },

        resize : function( c, wo ) {
            var index, borderWidth, setWidth, $hCells, $bCells, $fCells, $headers, $this, temp,
                $table = c.$table,
                $tableWrap = $table.parent(),
                $hdr = wo.scroller_$header,
                $foot = wo.scroller_$footer,
                id = c.namespace.slice( 1 ) + 'tsscroller',
            // Hide other scrollers so we can resize
                $div = $( 'div.' + tscss.scrollerWrap + '[id!="' + id + '"]' )
                    .addClass( tscss.scrollerHideElement );

            // Remove fixed so we get proper widths and heights
            ts.scroller.removeFixed( c, wo );

            // show original table thead to get proper alignments
            $table.children( 'thead' ).removeClass( tscss.scrollerHideElement );

            // Reset sizes so parent can resize.
            $table
                .addClass( tscss.scrollerReset )
                .children( 'thead' )
                .find( '.' + tscss.headerIn )
                .addClass( tscss.scrollerReset )
                .end()
                .find( '.' + tscss.filterRow )
                .removeClass( tscss.scrollerHideElement );
            $tableWrap.addClass( tscss.scrollerReset );

            // include left & right border widths
            borderWidth = parseInt( $table.css( 'border-left-width' ), 10 );

            $hCells = $hdr
                .children( 'thead' )
                .children( 'tr' )
                .not( '.' + c.cssIgnoreRow )
                .children( 'th, td' )
                .filter( ':visible' );
            $bCells = c.$tbodies
                .eq( 0 )
                .children( 'tr' )
                .not( '.' + c.cssChildRow )
                .eq( 0 )
                .children( 'th, td' )
                .filter( ':visible' );
            $fCells = $foot
                .children( 'tfoot' )
                .children( 'tr' )
                .children( 'th, td' )
                .filter( ':visible' );

            ts.scroller.setWidth( $hCells.add( $bCells ).add( $fCells ), '' );
            $headers = $table
                .children( 'thead' )
                .children()
                .eq( 0 )
                .children( 'th, td' );
            for ( index = 0; index < $headers.length; index++ ) {
                $this = $headers.eq( index );
                // code from https://github.com/jmosbech/StickyTableHeaders
                if ( $this.css( 'box-sizing' ) === 'border-box' ) {
                    setWidth = $this.outerWidth();
                } else {
                    if ( $hCells.eq( index ).css( 'border-collapse' ) === 'collapse' ) {
                        if ( $this.length && window.getComputedStyle ) {
                            setWidth = parseFloat( window.getComputedStyle( $this[ 0 ], null ).width );
                        } else {
                            // ie8 only
                            setWidth = $this.outerWidth() - parseFloat( $this.css( 'padding-left' ) ) -
                            parseFloat( $this.css( 'padding-right' ) ) -
                            ( parseFloat( $this.css( 'border-width' ) ) || 0 );
                        }
                    } else {
                        setWidth = $this.width();
                    }
                }
                temp = $hCells.eq( index )
                    .add( $bCells.eq( index ) )
                    .add( $fCells.eq( index ) );
                ts.scroller.setWidth( temp, setWidth );
            }

            temp = $tableWrap.parent().innerWidth() -
            ( ts.scroller.hasScrollBar( $tableWrap ) ? wo.scroller_barSetWidth : 0 );
            $tableWrap.width( temp );
            setWidth = $tableWrap.innerWidth() -
            ( ts.scroller.hasScrollBar( $tableWrap ) ? wo.scroller_barSetWidth : 0 ) + borderWidth;

            $hdr
                .parent()
                .add( $foot.parent() )
                .width( setWidth );

            wo.scroller_$container
                .find( '.' + tscss.scrollerReset )
                .removeClass( tscss.scrollerReset );

            // update fixed column sizes
            ts.scroller.updateFixed( c, wo );

            // hide original table thead
            $table.children( 'thead' ).addClass( tscss.scrollerHideElement );

            $div.removeClass( tscss.scrollerHideElement );

        },

        // Add fixed (frozen) columns (Do not call directly, use updateFixed)
        setupFixed : function( c, wo ) {
            var index, index2, $el, len, temp, $fixedColumn, $fixedTbody, $fixedContainer,
                $table = c.$table,
                $wrapper = wo.scroller_$container,
                fixedColumns = wo.scroller_fixedColumns;

            $fixedColumn = $wrapper
                .addClass( tscss.scrollerHasFix )
                .clone()
                .addClass( tscss.scrollerFixed )
                .removeClass( tscss.scrollerWrap )
                .attr( 'id', '' );

            if ( wo.scroller_addFixedOverlay ) {
                $fixedColumn.append( '<div class="' + tscss.scrollerFixedPanel + '">' );
            }

            $fixedTbody = $fixedColumn.find( '.' + tscss.scrollerTable );
            $fixedContainer = $fixedTbody.children( 'table' ).children( 'tbody' );
            $fixedTbody
                .children( 'table' )
                .addClass( c.namespace.slice( 1 ) + '_extra_table' )
                .attr( 'id', '' )
                .children( 'thead, tfoot' )
                .remove();

            wo.scroller_$fixedColumns = $fixedColumn;

            // RTL support (fixes column on right)
            if ( $table.hasClass( tscss.scrollerRtl ) ) {
                $fixedColumn.addClass( tscss.scrollerRtl );
            }

            $el = $fixedColumn.find( 'tr' );
            len = $el.length;
            for ( index = 0; index < len; index++ ) {
                $el.eq( index ).children( ':gt(' + ( fixedColumns - 1 ) + ')' ).remove();
            }
            $fixedColumn
                .addClass( tscss.scrollerHideElement )
                .prependTo( $wrapper );

            // look for filter widget
            if ( c.$table.hasClass( 'hasFilters' ) ) {
                // make sure fixed column filters aren't disabled
                $el = $fixedColumn
                    .find( '.' + tscss.filter )
                    .not( '.' + tscss.filterDisabled )
                    .prop( 'disabled', false );
                ts.filter.bindSearch( $table, $fixedColumn.find( '.' + tscss.filter ) );
                // disable/enable filters behind fixed column
                $el = $wrapper
                    .children( '.' + tscss.scrollerHeader )
                    .find( '.' + tscss.filter );
                len = $el.length;
                for ( index = 0; index < len; index++ ) {
                    // previously disabled filter; don't mess with it! filterDisabled class added by filter widget
                    if ( !$el.eq( index ).hasClass( tscss.filterDisabled || 'disabled' ) ) {
                        // disable filters behind fixed column; don't disable visible filters
                        $el.eq( index ).prop( 'disabled', index < fixedColumns );
                    }
                }
            }

            // disable/enable tab indexes behind fixed column
            c.$table
                .add( '.' + tscss.scrollerFooter + ' table' )
                .children( 'thead' )
                .children( 'tr.' + tscss.headerRow )
                .children()
                .attr( 'tabindex', -1 );

            $el = wo.scroller_$header
                .add( $fixedColumn.find( '.' + tscss.scrollerTable + ' table' ) )
                .children( 'thead' )
                .children( 'tr.' + tscss.headerRow );
            len = $el.length;
            for ( index = 0; index < len; index++ ) {
                temp = $el.eq( index ).children();
                for ( index2 = 0; index2 < temp.length; index2++ ) {
                    temp.eq( index2 ).attr( 'tabindex', index2 < fixedColumns ? -1 : 0 );
                }
            }

            ts.bindEvents( c.table, $fixedColumn.find( '.' + tscss.header ) );
            ts.scroller.bindFixedColumnEvents( c, wo );

            /*** Scrollbar hack! Since we can't hide the scrollbar with css ***/
            if ( ts.scroller.isFirefox || ts.scroller.isOldIE ) {
                $fixedTbody.wrap( '<div class="' + tscss.scrollerHack + '" style="overflow:hidden;">' );
            }

        },

        bindFixedColumnEvents : function( c, wo ) {
            // update thead & tbody in fixed column
            var namespace = c.namespace + 'tsscrollerFixed',
                events = ( 'tablesorter-initialized sortEnd filterEnd ' ).split( ' ' ).join( namespace + ' ' ),
                events2 = 'scroll' + namespace,
                $fixedTbody = wo.scroller_$fixedColumns.find( '.' + tscss.scrollerTable ),
                fixedScroll = true,
                tableScroll = true;

            c.$table
                .off( events )
                .on( events, function() {
                    ts.scroller.updateFixed( c, wo, false );
                    ts.scroller.resize( c, wo );
                })
                .parent()
                // *** SCROLL *** scroll fixed column along with main
                .off( events2 )
                .on( events2, function() {
                    // using flags to prevent firing the scroll event excessively leading to slow scrolling in Firefox
                    if ( fixedScroll || !ts.scroller.isFirefox ) {
                        tableScroll = false;
                        $fixedTbody[0].scrollTop = $( this ).scrollTop();
                        setTimeout( function() {
                            tableScroll = true;
                        }, 20 );
                    }
                });
            // scroll main along with fixed column
            $fixedTbody
                .off( events2 )
                .on( events2, function() {
                    // using flags to prevent firing the scroll event excessively leading to slow scrolling in Firefox
                    if ( tableScroll || !ts.scroller.isFirefox ) {
                        fixedScroll = false;
                        c.$table.parent()[0].scrollTop = $( this ).scrollTop();
                        setTimeout( function() {
                            fixedScroll = true;
                        }, 20 );
                    }
                })
                .scroll();

            // *** ROW HIGHLIGHT ***
            if ( wo.scroller_rowHighlight !== '' ) {
                events = 'mouseover mouseleave '.split( ' ' ).join( namespace + ' ' );
                // can't use c.$tbodies because it doesn't include info-only tbodies
                c.$table
                    .off( events, 'tbody > tr' )
                    .on( events, 'tbody > tr', function( event ) {
                        var indx = c.$table.children( 'tbody' ).children( 'tr' ).index( this );
                        $fixedTbody
                            .children( 'table' )
                            .children( 'tbody' )
                            .children( 'tr' )
                            .eq( indx )
                            .add( this )
                            .toggleClass( wo.scroller_rowHighlight, event.type === 'mouseover' );
                    });
                $fixedTbody
                    .find( 'table' )
                    .off( events, 'tbody > tr' )
                    .on( events, 'tbody > tr', function( event ) {
                        var $fixed = $fixedTbody.children( 'table' ).children( 'tbody' ).children( 'tr' ),
                            indx = $fixed.index( this );
                        c.$table
                            .children( 'tbody' )
                            .children( 'tr' )
                            .eq( indx )
                            .add( this )
                            .toggleClass( wo.scroller_rowHighlight, event.type === 'mouseover' );
                    });
            }
        },

        updateFixed : function( c, wo ) {
            var $wrapper = wo.scroller_$container;

            if ( wo.scroller_fixedColumns === 0 ) {
                ts.scroller.removeFixed( c, wo );
                return;
            }

            if ( !c.isScrolling ) {
                return;
            }

            // Make sure the wo.scroller_$fixedColumns container exists if not build it
            if ( !$wrapper.find( '.' + tscss.scrollerFixed ).length ) {
                ts.scroller.setupFixed( c, wo );
            }

            // scroller_fixedColumns
            var index, tbodyIndex, rowIndex, $tbody, $adjCol, $fb, $fixHead, $fixBody, $fixFoot,
                totalRows, widths, temp, adj, row,
                $table = c.$table,
                $tableWrap = $table.parent(),
                $hdr = wo.scroller_$header,
                $foot = wo.scroller_$footer,

            // source cells for measurement
                $mainTbodies = wo.scroller_$container
                    .children( '.' + tscss.scrollerTable )
                    .children( 'table' )
                    .children( 'tbody' ),
            // variable gets redefined
                $rows = wo.scroller_$header
                    .children( 'thead' )
                    .children( '.' + tscss.headerRow ),

            // hide fixed column during resize, or we get a FOUC
                $fixedColumn = wo.scroller_$fixedColumns
                    .addClass( tscss.scrollerHideElement ),

            // target cells
                $fixedTbodiesTable = $fixedColumn
                    .find( '.' + tscss.scrollerTable )
                    .children( 'table' ),
                $fixedTbodies = $fixedTbodiesTable
                    .children( 'tbody' ),
            // variables
                tsScroller = ts.scroller,
                scrollBarWidth = wo.scroller_barSetWidth,
                fixedColumns = wo.scroller_fixedColumns,
                dir = $table.hasClass( tscss.scrollerRtl ),
            // get dimensions
                $temp = $table.find( 'tbody td' ),
                borderRightWidth = parseInt( $temp.css( 'border-right-width' ), 10 ) || 1,
                borderSpacing = parseInt( ( $temp.css( 'border-spacing' ) || '' ).split( /\s/ )[ 0 ], 10 ) / 2 || 0,
                totalWidth = parseInt( $table.css( 'padding-left' ), 10 ) +
                    parseInt( $table.css( 'padding-right' ), 10 ) -
                    borderRightWidth;

            ts.scroller.removeFixed( c, wo, false );

            // recalculate widths
            $table.children( 'thead' ).removeClass( tscss.scrollerHideElement );
            widths = [];
            for ( index = 0; index < c.columns; index++ ) {
                temp = c.$headerIndexed[ index ].outerWidth();
                totalWidth += index < fixedColumns ? temp + borderSpacing : 0;
                widths.push( temp );
            }
            $table.children( 'thead' ).addClass( tscss.scrollerHideElement );

            // set fixed column width
            totalWidth = totalWidth + borderRightWidth * 2 - borderSpacing;
            tsScroller.setWidth( $fixedColumn.add( $fixedColumn.children() ), totalWidth );
            tsScroller.setWidth( $fixedColumn.children().children( 'table' ), totalWidth );

            $table.find( '.' + tscss.scrollerSpacerRow ).remove();
            row = '<tr class="' + tscss.scrollerSpacerRow + ' ' + c.selectorRemove.slice(1) + '">';
            for ( index = 0; index < c.columns; index++ ) {
                row += '<td style="padding:0; margin:0;height:0;max-height:0;min-height:0;width:' +
                widths[ index ] + 'px;min-width:' + widths[ index ] + 'px;max-width:' +
                widths[ index ] + 'px"></td>';
            }
            c.$tbodies.eq(0).prepend( row += '</tr>' );

            // update fixed column tbody content, set row height & set cell widths for first row
            for ( tbodyIndex = 0; tbodyIndex < c.$tbodies.length; tbodyIndex++ ) {
                $tbody = $mainTbodies.eq( tbodyIndex );
                if ( $tbody.length ) {
                    // get tbody
                    $rows = $tbody.children();
                    totalRows = $rows.length;
                    $fb = ts.processTbody( $fixedTbodiesTable, $fixedTbodies.eq( tbodyIndex ), true );
                    $fb.empty();
                    // update tbody cells after sort/filtering
                    for ( rowIndex = 0; rowIndex < totalRows; rowIndex++ ) {
                        $adjCol = $( $rows[ rowIndex ].outerHTML );
                        $adjCol
                            .children( 'td, th' )
                            .slice( fixedColumns )
                            .remove();
                        $fb.append( $adjCol );
                    }
                    // adjust fixed thead/tbody/tfoot cell widths
                    $fixHead = $fixedColumn
                        .find( 'thead' )
                        .children( 'tr.' + tscss.headerRow )
                        .children();
                    $fixBody = $fixedColumn
                        .find( tscss.scrollerSpacerRow )
                        .children();
                    $fixFoot = $fixedColumn
                        .find( 'tfoot' )
                        .children( 'tr' )
                        .eq( 0 )
                        .children();
                    // reusing variables, so ignore the names :P
                    $adjCol = $hdr.children( 'thead' ).children( 'tr' ).children( 'td, th' );
                    $rows = $foot.children( 'tfoot' ).children( 'tr' ).children( 'td, th' );
                    for ( index = 0; index < c.columns; index++ ) {
                        if ( index < fixedColumns ) {
                            $temp = $fixHead.eq( index )
                                .add( $fixBody.eq( index ) )
                                .add( $fixFoot.eq( index ) );
                            tsScroller.setWidth( $temp, widths[ index ] );
                        }
                        $temp = $adjCol.eq( index )
                            .add( $rows.eq( index ) );
                        tsScroller.setWidth( $temp, widths[ index ] );
                    }

                    // restore tbody
                    ts.processTbody( $fixedTbodiesTable, $fb, false );
                }
            }

            /*** scrollbar HACK! Since we can't hide the scrollbar with css ***/
            if ( tsScroller.isFirefox || tsScroller.isOldIE ) {
                $fixedTbodiesTable
                    .parent()
                    .css({
                        'width' : totalWidth
                    });
            }

            $fixedColumn.removeClass( tscss.scrollerHideElement );
            for ( index = 0; index < fixedColumns; index++ ) {
                $wrapper
                    .children( 'div' )
                    .children( 'table' )
                    .find( 'th:nth-child(' + ( index + 1 ) + '), td:nth-child(' + ( index + 1 ) + ')' )
                    .addClass( tscss.scrollerHideColumn );
            }

            adj = ts.scroller.hasScrollBar( $tableWrap ) ? scrollBarWidth : 0;
            totalWidth = totalWidth - borderRightWidth;
            temp = $tableWrap.parent().innerWidth() - totalWidth;
            $tableWrap.width( temp );
            // RTL support (fixes column on right)
            $wrapper
                .children( '.' + tscss.scrollerTable )
                .css( dir ? 'right' : 'left', totalWidth );
            $wrapper
                .children( '.' + tscss.scrollerHeader + ', .' + tscss.scrollerFooter )
                // Safari needs a scrollbar width of extra adjusment to align the fixed & scrolling columns
                .css( dir ? 'right' : 'left', totalWidth + ( dir && ts.scroller.isSafari ? adj : 0 ) );

            $hdr
                .parent()
                .add( $foot.parent() )
                .width( temp - adj );

            // fix gap under the tbody for the horizontal scrollbar
            temp = ts.scroller.hasScrollBar( $tableWrap, true );
            adj = temp ? scrollBarWidth : 0;
            if ( !$fixedColumn.find( '.' + tscss.scrollerBarSpacer ).length && temp ) {
                $temp = $( '<div class="' + tscss.scrollerBarSpacer + '">' )
                    .css( 'height', adj + 'px' );
                $fixedColumn.find( '.' + tscss.scrollerTable ).append( $temp );
            } else if ( !temp ) {
                $fixedColumn.find( '.' + tscss.scrollerBarSpacer ).remove();
            }

            ts.scroller.updateRowHeight( c, wo );
            // set fixed column height (changes with filtering)
            $fixedColumn.height( $wrapper.height() );

            $fixedColumn.removeClass( tscss.scrollerHideElement );

        },

        fixHeight : function( $rows, $fixedRows ) {
            var index, heightRow, heightFixed, $r, $f,
                len = $rows.length;
            for ( index = 0; index < len; index++ ) {
                $r = $rows.eq( index );
                $f = $fixedRows.eq( index );
                heightRow = $r.height();
                heightFixed = $f.height();
                if ( heightRow > heightFixed ) {
                    $f.addClass( tscss.scrollerAddedHeight ).height( heightRow );
                } else if ( heightRow < heightFixed ) {
                    $r.addClass( tscss.scrollerAddedHeight ).height( heightFixed );
                }
            }
        },

        updateRowHeight : function( c, wo ) {
            var $rows, $fixed,
                $fixedColumns = wo.scroller_$fixedColumns;

            wo.scroller_$container
                .find( '.' + tscss.scrollerAddedHeight )
                .removeClass( tscss.scrollerAddedHeight )
                .height( '' );

            $rows = wo.scroller_$header
                .children( 'thead' )
                .children( 'tr' );
            $fixed = $fixedColumns
                .children( '.' + tscss.scrollerHeader )
                .children( 'table' )
                .children( 'thead' )
                .children( 'tr' );
            ts.scroller.fixHeight( $rows, $fixed );

            $rows = wo.scroller_$footer
                .children( 'tfoot' )
                .children( 'tr' );
            $fixed = $fixedColumns
                .children( '.' + tscss.scrollerFooter )
                .children( 'table' )
                .children( 'tfoot' )
                .children( 'tr' );
            ts.scroller.fixHeight( $rows, $fixed );

            if ( ts.scroller.isFirefox ) {
                // Firefox/Old IE scrollbar hack (wraps table to hide the scrollbar)
                $fixedColumns = $fixedColumns.find( '.' + tscss.scrollerHack );
            }
            $rows = c.$table
                .children( 'tbody' )
                .children( 'tr' );
            $fixed = $fixedColumns
                .children( '.' + tscss.scrollerTable )
                .children( 'table' )
                .children( 'tbody' )
                .children( 'tr' );
            ts.scroller.fixHeight( $rows, $fixed );

        },

        removeFixed : function( c, wo, removeIt ) {
            var $table = c.$table,
                $wrapper = wo.scroller_$container,
                dir = $table.hasClass( tscss.scrollerRtl );

            // remove fixed columns
            if ( removeIt || typeof removeIt === 'undefined' ) {
                $wrapper.find( '.' + tscss.scrollerFixed ).remove();
            }

            $wrapper
                .find( '.' + tscss.scrollerHideColumn )
                .removeClass( tscss.scrollerHideColumn );

            // RTL support ( fixes column on right )
            $wrapper
                .children( ':not(.' + tscss.scrollerFixed + ')' )
                .css( dir ? 'right' : 'left', 0 );
        },

        remove : function( c, wo ) {
            var $wrap = wo.scroller_$container,
                namespace = c.namespace + 'tsscroller';
            c.$table
                .off( namespace )
                .insertBefore( $wrap )
                .find( 'thead' )
                .removeClass( tscss.scrollerHideElement )
                .children( 'tr.' + tscss.headerRow )
                .children()
                .attr( 'tabindex', 0 )
                .end()
                .find( '.' + tscss.filterRow )
                .removeClass( tscss.scrollerHideElement + ' ' + tscss.filterRowHide );
            c.$table
                .find( '.' + tscss.filter )
                .not( '.' + tscss.filterDisabled )
                .prop( 'disabled', false );
            $wrap.remove();
            $( window ).off( namespace );
            c.isScrolling = false;
        }

    };

})( jQuery, window );
