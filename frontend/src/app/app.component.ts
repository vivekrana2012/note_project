import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VideoService, VideoInfo } from './video.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  videos: VideoInfo[] = [];
  loading = true;
  error = '';

  constructor(private videoService: VideoService) {}

  ngOnInit() {
    this.loadVideos();
  }

  loadVideos() {
    this.videoService.getVideos().subscribe({
      next: (data) => {
        this.videos = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load videos';
        this.loading = false;
        console.error(err);
      }
    });
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
}
