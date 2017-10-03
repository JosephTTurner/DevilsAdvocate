'use strict';

const gulp    = require('gulp');
const eslint  = require('gulp-eslint');
const plumber = require('gulp-plumber');
const sketch  = require('gulp-sketch');

// JS Source
const JS_SOURCE = [
	'./js/content-scripts.js',
	'./js/popup.js',
	'!./js/jquery-2.2.4.min.js'
];

// ESLint
gulp.task('lint', function() {
	return gulp.src(JS_SOURCE)
		.pipe(plumber())
		.pipe(eslint({
			rules: {
				'strict': 2
			},
			globals: [
				'jQuery',
				'$'
			],
			envs: [
				'browser'
			]
		}))
		.pipe(eslint.format())
		.pipe(eslint.failAfterError());
});

// Sketch
gulp.task('sketch', function() {
	return gulp.src(['./*.sketch'])
		.pipe(sketch({
			export: 'slices',
			formats: 'png'
		}))
		.pipe(gulp.dest('./img'));
});

// Watch
gulp.task('watch', ['lint', 'sketch'], function() {
	gulp.watch(JS_SOURCE, ['lint']);
	gulp.watch(['./*.sketch'], ['sketch']);
});

// Default
gulp.task('default', function() {
	gulp.start('watch');
});