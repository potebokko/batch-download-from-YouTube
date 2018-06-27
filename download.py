from pytube import Playlist, YouTube
from pytube.exceptions import RegexMatchError
from manage_files import FileManager

# YouTubeダウンローダー
class YtubeDownloader():
    # 動画をダウンロードする
    def download_video(self,video_url,save_dir):
        print("Downloading:",video_url)
        YouTube(video_url).streams.first().download(save_dir)

    # プレイリストをダウンロードする
    def download_playlist(self,playlist_url,save_dir):
        print("Downloading:",playlist_url)
        Playlist(playlist_url).download_all(save_dir)

    # URLに対応してダウンロードする
    def download_something(self,any_url_list,save_dir):
        # リストを掘りながらそれぞれをダウンロードする
        for any_url in any_url_list:
            try:
                self.download_video(any_url,save_dir)
            except RegexMatchError:
                print("Failed, this is playlist")
                self.download_playlist(any_url,save_dir)

# 使用例
if __name__ == "__main__":
    fm = FileManager()
    dir_name = fm.make_unique_dir()
    print("Enter URLs")
    print("If you want to end, type 'exit'")
    input_list = []

    # 標準入力から複数のURLを得てリストに格納する
    while(True):
        input_str = input()
        if input_str == "exit":
            break
        else:
            input_list.append(input_str)

    # ダウンローダークラスを作成
    downloader = YtubeDownloader()
    # URLに対応してダウンロードする
    downloader.download_something(input_list,dir_name)
