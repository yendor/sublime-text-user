import sublime, sublime_plugin, webbrowser, re

class HelpForWordCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # define lookups here
    urls = {
      # r'scope\.name\.regex': 'http://url.for/%(function_name)s'
      r'support\.function\..+\.php': 'http://php.net/%s',
      r'support\.function\.perl': 'http://perldoc.perl.org/functions/%s.html',
      r'(storage\..+|keyword\..+|support\..+|constant\.language)\.python': 'http://effbot.org/pyref/%s.htm',
      r'meta\.tag\.(inline|block)\.any\.html': 'http://www.htmldog.com/reference/htmltags/%s/'
    }

    for region in self.view.sel():
      scopes = self.view.scope_name(region.begin()).strip().split(' ')

      if region.empty():
        p = region.begin()

        # html specifics
        if self.view.scope_name(p).find('text.html.basic') > -1 and self.view.scope_name(p).find('embedded.block.html') == -1:
          while p >= 0:
            if self.view.substr(p) == '<' and self.view.scope_name(p).find('string.quoted.double.html') < 0:
              p += 1

              # check if it's an end tag
              if self.view.substr(p) == '/':
                p += 1

              break

            else:
              p -= 1

        s = self.view.substr(self.view.word(p))

      else:
        s = self.view.substr(region)

      for scope in scopes:
        for search in urls.keys():
          if re.search(search, scope):
            webbrowser.open_new_tab(urls[search] % s)
            return

      else:
        # purloined from: http://www.sublimetext.com/forum/posting.php?mode=reply&f=5&t=2242
        language = self.view.scope_name(self.view.sel()[0].begin()).strip().split('.')[-1]

        webbrowser.open_new_tab('http://www.google.com/search?q=%s' % (s + ' ' + language))