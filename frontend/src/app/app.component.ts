import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VideoService, VideoInfo } from './video.service';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  videos: VideoInfo[] = [];
  loading = true;
  error = '';
  selectedVideo: VideoInfo | null = null;
  summaryData: any = null;
  loadingSummary = false;

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

  viewSummary(video: VideoInfo) {
    this.selectedVideo = video;
    this.loadingSummary = true;
    this.summaryData = null;

    this.videoService.getVideoSummary(video.video_id).subscribe({
      next: (data) => {
        this.summaryData = data;
        this.loadingSummary = false;
      },
      error: (err) => {
        console.error('Failed to load summary', err);
        this.loadingSummary = false;
      }
    });
  }

  closeSummary() {
    this.selectedVideo = null;
    this.summaryData = null;
  }
}
