/**
 * @jest-environment jsdom
 */

/* eslint import/extensions: [0, {}] */
/* eslint import/no-unresolved: [0, {}] */

import 'routes/resolver';


describe('resolver', () => {
  beforeEach(() => {
    window.routes = {
      home: '/',
      home_with_one_positional_arg: '/home/positional/<>/ping/',
      home_with_many_positional_args: '/home/positional/<>/ping/<>/pong/',
      home_with_one_named_arg: '/home/named/<year>/ping/',
      home_with_many_named_args: '/home/named/<year>/ping/<month>/pong/',
    };
  });

  test('can resolve a route without argument', () => {
    expect(window.reverseUrl('home')).toEqual('/');
  });

  test('can resolve a route containing a positional argument', () => {
    expect(window.reverseUrl('home_with_one_positional_arg', 42))
      .toEqual('/home/positional/42/ping/');
  });

  test('can resolve a route containing many positional arguments', () => {
    expect(window.reverseUrl('home_with_many_positional_args', 'foo', 'bar'))
      .toEqual('/home/positional/foo/ping/bar/pong/');
  });

  test('can resolve a route containing many positional arguments using an array', () => {
    expect(window.reverseUrl('home_with_many_positional_args', ['foo', 'bar']))
      .toEqual('/home/positional/foo/ping/bar/pong/');
  });

  test('can resolve a route containing a named argument', () => {
    expect(window.reverseUrl('home_with_one_named_arg', { year: 2001 }))
      .toEqual('/home/named/2001/ping/');
  });

  test('can resolve a route containing many named arguments', () => {
    expect(window.reverseUrl('home_with_many_named_args', { year: 2001, month: 12 }))
      .toEqual('/home/named/2001/ping/12/pong/');
  });

  test('throws if the URL name is not known', () => {
    expect(() => window.reverseUrl('unknown', { year: 2001, month: 12 }))
      .toThrowError("URL 'unknown' was not found.");
  });

  test('throws if the number of positional arguments does not match the expected arguments', () => {
    expect(() => window.reverseUrl('home_with_many_positional_args', 'foo', 'bar', '1', '2', '3'))
      .toThrowError('Invalid URL lookup: Wrong number of arguments ; expected 2 arguments.');
    expect(() => window.reverseUrl('home_with_many_positional_args', ['foo', 'bar', '1', '2', '3']))
      .toThrowError('Invalid URL lookup: Wrong number of arguments ; expected 2 arguments.');
  });

  test('throws if an expected named argument is not provided', () => {
    expect(() => window.reverseUrl('home_with_many_named_args', { year: 2001 }))
      .toThrowError("Invalid URL lookup: Argument 'month' was not provided.");
  });

  test('throws if an URL without argument is resolved with unexpected arguments', () => {
    expect(() => window.reverseUrl('home', { year: 2001 }))
      .toThrowError("Invalid URL lookup: URL 'home' does not expect any arguments.");
    expect(() => window.reverseUrl('home', 'foo', 'bar'))
      .toThrowError("Invalid URL lookup: URL 'home' does not expect any arguments.");
    expect(() => window.reverseUrl('home', ['foo', 'bar']))
      .toThrowError("Invalid URL lookup: URL 'home' does not expect any arguments.");
  });
});
