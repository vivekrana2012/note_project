import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { VideoService, VideoInfo } from '../video.service';

@Component({
  selector: 'app-video-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './video-summary.component.html',
  styleUrls: ['./video-summary.component.css']
})
export class VideoSummaryComponent implements OnInit {
  videoId: string = '';
  videoInfo: VideoInfo | null = null;
  summaryData: any = null;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private videoService: VideoService
  ) {
    // Get video data from navigation state
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      this.videoInfo = navigation.extras.state['video'];
    }
  }

  ngOnInit() {
    this.videoId = this.route.snapshot.paramMap.get('id') || '';
    if (this.videoId) {
      this.loadSummary();
    }
  }

  loadSummary() {
    this.videoService.getVideoSummary(this.videoId).subscribe({
      next: (data) => {
        this.summaryData = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load summary';
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
