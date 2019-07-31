var gulp = require('gulp');

gulp.task('sass', function () {
    const sass = require('gulp-sass');
    sass.compiler = require('node-sass');
    return gulp.src('./theme/sass/**/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('./assets/static/css/'));
});

gulp.task('uncss', function () {
    const postcss = require('gulp-postcss');
    const uncss = require('postcss-uncss');
    return gulp.src('./assets/static/css/kendinicinkodla.css')
        .pipe(postcss([
            uncss({
                html: ['./_build/**/*.html'],
                ignore: [
                    new RegExp('\.modal'),
                    new RegExp('\.card\.workshop')
                ]
            })
        ]))
        .pipe(gulp.dest('./theme/css/'));
});

gulp.task('cssmin', function () {
    const cssmin = require('gulp-cssmin');
    return gulp.src('./theme/css/kendinicinkodla.css')
        .pipe(cssmin())
        .pipe(gulp.dest('./assets/static/css/'));
});

gulp.task('build', gulp.series('sass'));
gulp.task('after_build', gulp.series('uncss', 'cssmin'));
gulp.task('watch', function () {
    return gulp.watch('./theme/sass/**/*.scss', gulp.series('build', 'after_build'));
});

gulp.task('default', gulp.series('build'));
