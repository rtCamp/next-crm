import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import path from 'path'
import { VitePWA } from 'vite-plugin-pwa'
import frappeui from 'frappe-ui/vite'

export default defineConfig(async ({ mode }) => {
  
  const env = loadEnv(mode, process.cwd())
  let proxyConfig = {}

  if (env.VITE_SITE_NAME && env.VITE_SITE_PORT) {
    proxyConfig = {
      '^/(app|api|assets|files|private)': {
        target: `http://${env.VITE_SITE_NAME}:${env.VITE_SITE_PORT}`,
        ws: true,
        changeOrigin: true,
        secure: false,
      },
    }
  }
  return {
    server: {
      port: 8080,
      proxy: proxyConfig,
    },
    plugins: [
      frappeui({
        frappeProxy: true,
        lucideIcons: true,
        jinjaBootData: true,
        buildConfig: {
          indexHtmlPath: '../next_crm/www/next-crm/index.html',
          emptyOutDir: true,
          sourcemap: true,
        },
      }),
      vue({
        script: {
          propsDestructure: true,
        },
      }),
      vueJsx(),
      VitePWA({
        registerType: 'autoUpdate',
        devOptions: {
          enabled: true,
        },
        manifest: {
          display: 'standalone',
          name: 'Next CRM',
          short_name: 'Next CRM',
          start_url: '/next-crm',
          description: 'Modern & 100% Open-source CRM tool to supercharge your sales operations',
          icons: [
            {
              src: '/assets/next_crm/manifest/manifest-icon-192.maskable.png',
              sizes: '192x192',
              type: 'image/png',
              purpose: 'any',
            },
            {
              src: '/assets/next_crm/manifest/manifest-icon-192.maskable.png',
              sizes: '192x192',
              type: 'image/png',
              purpose: 'maskable',
            },
            {
              src: '/assets/next_crm/manifest/manifest-icon-512.maskable.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'any',
            },
            {
              src: '/assets/next_crm/manifest/manifest-icon-512.maskable.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'maskable',
            },
          ],
        },
        workbox: {
          maximumFileSizeToCacheInBytes: 4 * 1024 * 1024, // 4 MiB
        }
      }),
      {
        name: 'transform-index.html',
        transformIndexHtml(html, context) {
          if (!context.server) {
            return html.replace(
              /<\/body>/,
              `
                  <script>
                      {% for key in boot %}
                      window["{{ key }}"] = {{ boot[key] | tojson }};
                      {% endfor %}
                  </script>
                  </body>
                  `,
            )
          }
          return html
        },
      },
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    build: {
      outDir: '../next_crm/public/frontend',
      emptyOutDir: true,
      sourcemap: true,
    },
    optimizeDeps: {
      include: ['feather-icons', 'showdown', 'tailwind.config.js', 'engine.io-client', 'prosemirror-state', "highlight.js/lib/core", 'prosemirror-view',
        'lowlight'],
    },
  }
})
