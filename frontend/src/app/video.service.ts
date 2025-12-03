import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface VideoInfo {
  video_id: string;
  url: string;
  title: string;
  publish_date: string;
  timestamp: string;
  file: string;
  path: string;
}

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  constructor(private http: HttpClient) {}

  getVideos(): Observable<VideoInfo[]> {
    return this.http.get<VideoInfo[]>('/videos');
  }

  getVideoSummary(videoId: string): Observable<any> {
    return this.http.get(`/videos/${videoId}`);
  }
}
