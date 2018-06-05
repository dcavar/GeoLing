# ----------------------------------------------------------------------
# config file for SASS/Compass
# http://beta.compass-style.org/help/tutorials/configuration-reference/
# ----------------------------------------------------------------------

# Require any additional compass plugins here.

# Set this to the root of your project when deployed:
http_path       = "/"
project_path    = "."
sass_dir        = "geoevent/static/geoevent/scss"
css_dir         = "geoevent/static/geoevent/css"
images_dir      = "geoevent/static/geoevent/img"
#javascripts_dir = "geoevent/static/geoevent/js"

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :expanded or :nested or :compact or :compressed
# build compass for production
# compass compile -e production --force
# output_style    = (environment == :production) ? :compressed : :expanded
output_style    = :compressed

# To enable relative paths to assets via compass helper functions. Uncomment:
# relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
line_comments = false


# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass sass scss && rm -rf sass && mv scss sass

# toggle between the sass or scss syntax
sass_options = {
  :syntax => :scss
}
