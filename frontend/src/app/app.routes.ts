import { Routes } from '@angular/router';
import { VideoListComponent } from './video-list/video-list.component';
import { VideoSummaryComponent } from './video-summary/video-summary.component';

export const routes: Routes = [
  { path: '', component: VideoListComponent },
  { path: 'video/:id', component: VideoSummaryComponent },
  { path: '**', redirectTo: '' }
];
