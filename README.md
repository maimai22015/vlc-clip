# vvlc-clip
<!-- wp:heading -->
<h2>概要</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>動画を再生しながら素材集めをしたいときに便利なスクリプトです。動画を再生中、ボタンを押すと（あるいは設定したキーを押すと）ボタンを押した瞬間前後の指定した範囲を別の動画ファイルとして書き出すコマンドを生成、実行することができます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>このスクリプトについて</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>過去にVLC-animeという同目的のスクリプトを開発し、公開していますが、互換性はありません。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>ver 1 (現在非公開) ：python-vlcを用いたメディアプレーヤー。コードが難解で開発に行き詰まり諦め</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>ver 2 (<a rel="noreferrer noopener" href="https://ytpmv.info/vlc-anime/" target="_blank">https://ytpmv.info/vlc-anime/</a>) ：VLCの拡張機能として作成。lua言語。VLC側で私の求める機能が実装されていない（削除された）ためver 3の開発を決断。ver 2を使ってもいいよ。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>ver 3 (ココ)：VLCのremote control interfaceをPythonで操作。python-vlcを用いないためexe化が可能になった。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>ダウンロード</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><a href="https://github.com/maimai22015/vlc-anime-v3/releases" data-type="URL" data-id="https://github.com/maimai22015/vlc-anime-v3/releases" target="_blank" rel="noreferrer noopener">https://github.com/maimai22015/vlc-anime-v3/releases</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Python版とexe版が含まれます。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Python版を用いる場合は、以下のライブラリを導入してください</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>PySimpleGUI&nbsp;</li></ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>参考</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>このスクリプトの作成にあたり、以下のコードを参考にしています</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>https://stackoverflow.com/a/61485122</li><li>https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Media_Player_VLC_Based.py</li></ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>導入</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>VLCをインストールしていることが必要です。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>書き出し時にffmpegを使用します。<a rel="noreferrer noopener" href="https://ffmpeg.org/download.html" target="_blank">https://ffmpeg.org/download.html</a>より各自の環境に合わせてダウンロードしてください。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Python版では、インストールしていないライブラリがある場合は導入してください。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Python版、exe版共通して、setting.iniの内容を各自の環境に合わせて変更してください。</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>キーコンフィグについて</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>私の場合はテンキーで操作することを前提に作成しているため、それ用の設定にしてあります。各自使いやすいように設定してください。引用符無しでkey_〇〇 = a の形になるように記入してください。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>使い方</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>まずコマンドプロンプトを起動し、VLCをインストールしたフォルダで以下のコマンドを実行します。</p>
<!-- /wp:paragraph -->

<!-- wp:enlighter/codeblock -->
<pre class="EnlighterJSRAW" data-enlighter-language="generic" data-enlighter-theme="" data-enlighter-highlight="" data-enlighter-linenumbers="" data-enlighter-lineoffset="" data-enlighter-title="" data-enlighter-group="">vlc --intf rc --rc-host 127.0.0.1:44500</pre>
<!-- /wp:enlighter/codeblock -->

<!-- wp:paragraph -->
<p>これを行わない場合、ウィンドウが応答しなくなります。</p>
<!-- /wp:paragraph -->

<!-- wp:image {"align":"center","id":1077,"sizeSlug":"large","linkDestination":"none"} -->
<div class="wp-block-image"><figure class="aligncenter size-large"><img src="https://ytpmv.info/wp-content/uploads/2021/01/image-1.png" alt="" class="wp-image-1077"/><figcaption>こんな感じでショートカットを作成すると便利かもしれません。</figcaption></figure></div>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p>次にスクリプトを実行します。</p>
<!-- /wp:paragraph -->

<!-- wp:image {"align":"center","id":1076,"sizeSlug":"large","linkDestination":"none"} -->
<div class="wp-block-image"><figure class="aligncenter size-large"><img src="https://ytpmv.info/wp-content/uploads/2021/01/image.png" alt="" class="wp-image-1076"/></figure></div>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p>loadボタンを押し、ファイルを選択。再生が始まります。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>動画を再生しつつ、切り出したいシーンを見つけたらcutボタンを押します。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>切り出したいシーンをすべて見つけ、それぞれでcutボタンを押したら、最後にGenerate&nbsp;.bat&nbsp;and&nbsp;runボタンを押します。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>別ウィンドウでコマンドが実行されます。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>ファイルを続けて再生するときは、1ファイル再生が終わるたびにStopボタンを押してください。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>もしファイルが出力されていない場合は、再生していた動画ファイルと同じフォルダにコマンドが記載されたbatファイルが生成されるので、それを確認してください。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>他にも、再生速度の調整、スキップ、戻る、一時停止の機能があります。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>以上。活用してね。</p>
<!-- /wp:paragraph -->
