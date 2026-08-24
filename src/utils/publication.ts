type PublicationData = {
  draft?: boolean;
  status?: string;
  publishDate?: Date;
  publish_at?: string;
  fact_check_status?: string;
  alan_approval?: string;
  image_status?: string;
};

export function publicationTime(data: PublicationData): Date {
  return data.publishDate || new Date(data.publish_at || 0);
}

export function isPublishable(data: PublicationData, now = new Date()): boolean {
  if (data.draft) return false;
  if (!data.status) return publicationTime(data) <= now;
  return ['scheduled', 'published'].includes(data.status)
    && data.alan_approval === 'approved'
    && data.fact_check_status === 'verified'
    && data.image_status === 'ready'
    && publicationTime(data) <= now;
}
