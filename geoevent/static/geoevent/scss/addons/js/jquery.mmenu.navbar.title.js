/*	
 * jQuery mmenu navbar addon title content
 * mmenu.frebsite.nl
 *
 * Copyright (c) Fred Heusschen
 */

(function( $ ) {

	var _PLUGIN_ 	= 'mmenu',
		_ADDON_  	= 'navbars',
		_CONTENT_	= 'title';

	$[ _PLUGIN_ ].addons[ _ADDON_ ][ _CONTENT_ ] = function( $navbar, opts )
	{
		//	Get vars
		var _c = $[ _PLUGIN_ ]._c;


		//	Add content
		$navbar.append( '<a class="' + _c.title + '"></a>' );


		//	Update
		var update = function( $panel )
		{
			$panel = $panel || this.$pnls.children( '.' + _c.current );

			var $node = $navbar.find( '.' + _c.title ),
				$orgn = $panel.find( '.' + this.conf.classNames[ _ADDON_ ].panelTitle );

			if ( !$orgn.length )
			{
				$orgn = $panel.children( '.' + _c.navbar ).children( '.' + _c.title );
			}

			var _url = $orgn.attr( 'href' ),
				_txt = $orgn.html() || opts.title;

			$node[ _url ? 'attr' : 'removeAttr' ]( 'href', _url );
			$node[ _url || _txt ? 'removeClass' : 'addClass' ]( _c.hidden );
			$node.html( _txt );
		};

		this.bind( 'openPanel', update );
		this.bind( 'init',
			function()
			{
				update.call( this );
			}
		);
	};

})( jQuery );