vim devops-final-exam/templates/_helpers.tpl
  {{/* This is a comment - Generate basic labels */}}
  {{- define "devops.labels" }}
  generator: helm
  date: {{ now | htmlDate }}
  name: {{ .Release.Name }}
  {{- include "devops.labels" . | nindent 4 }}
{{- end }}
  
 

