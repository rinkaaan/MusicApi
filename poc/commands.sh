# Download video as m4a with thumbnail
yt-dlp -x --audio-format m4a --embed-thumbnail --write-thumbnail --output "%(title)s.%(ext)s" [URL]
