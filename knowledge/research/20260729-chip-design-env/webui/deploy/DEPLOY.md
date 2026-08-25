# Deploy

- URL: https://chip-design.team-attention.com
- Vercel project: chip-design-env (koomooks-projects), alias https://chip-design-env.vercel.app
- Source: ../index.html → deploy/index.html (copy before redeploy)
- Redeploy: `cd deploy && npx vercel --prod --yes --name chip-design-env`
- DNS: Google Cloud DNS zone `teamattention-zone-primary` (GCP project teamattention)
  - CNAME chip-design.team-attention.com → 02285d6d844d8ca1.vercel-dns-016.com. (TTL 300)
  - Add command: /opt/homebrew/share/google-cloud-sdk/bin/gcloud dns record-sets create chip-design.team-attention.com. --zone=teamattention-zone-primary --type=CNAME --ttl=300 --rrdatas=02285d6d844d8ca1.vercel-dns-016.com. --project=teamattention
- Deployed: 2026-07-30
