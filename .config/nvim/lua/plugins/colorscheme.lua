-- return {
--   -- add gruvbox
--
--
--   -- Configure LazyVim to load gruvbox
--   {
--     "LazyVim/LazyVim",
--     init = function()
--       local clear_background = function()
--         local groups = {
--           "Normal",
--           "NormalNC",
--           "EndOfBuffer",
--           "SignColumn",
--           "LineNr",
--           "FoldColumn",
--           "CursorLineNr",
--           "NormalFloat",
--           "FloatBorder",
--         }
--
--         for _, group in ipairs(groups) do
--           vim.api.nvim_set_hl(0, group, { bg = "none" })
--         end
--       end
--
--       vim.api.nvim_create_autocmd("ColorScheme", {
--         callback = clear_background,
--       })
--
--       vim.schedule(clear_background)
--     end,
--     opts = {
--       colorscheme = "base16-grayscale-dark",
--     },
--   },
-- }

return {
  { "typicode/bg.nvim", lazy = false },
  { "nyoom-engineering/oxocarbon.nvim" },
  { "RRethy/nvim-base16" },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "base16-grayscale-dark",
    },
  },
}
