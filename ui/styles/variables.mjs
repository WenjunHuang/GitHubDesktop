import * as Colors from "color_system.mjs"


export const overlay_background_color = Colors.hexPlusAlpha('#000', 0.4)
export const color_deleted = Colors.red
export const color_modified = Colors.getColor('yellow', '700')
export const color_renamed = Colors.blue
export const color_conflicted = Colors.orange

export const text_color = Colors.getColor('gray', '900')
export const text_secondary_color = Colors.getColor('gray', '500')
export const background_color = Colors.white

export const button_height = 25
export const button_background = Colors.blue
export const button_border_radius = 2
export const button_hover_background = Colors.lighter(Colors.blue, 0.05)
export const button_text_color = Colors.white
export const button_focus_border_color = Colors.getColor('blue', '600')

export const link_button_color = Colors.blue
export const link_button_hover_color = Colors.getColor('blue', '600')

export const secondary_button_background = Colors.getColor('gray', '000')
export const secondary_button_hover_background = Colors.white
export const secondary_button_text_color = text_color
export const secondary_button_focus_shadow_color = Colors.hexPlusAlpha(Colors.getColor('gray', '200'), 0.75)
export const secondary_button_focus_border_color = Colors.getColor('gray', '300')

/**
 * Color for icons that are placed on top of a colored backing
 * (like a circle badge icon)
 */
export const badge_icon_color = Colors.white


export const scroll_bar_thumb_background_color = Colors.hexPlusAlpha('#000', 0.2)
export const scroll_bar_thumb_background_color_active = Colors.hexPlusAlpha('#000', 0.5)

// Box
//
// We use the term 'box' here to refer to a very high-level generic
// component that fits many use cases. A 'box' might be a list item
// or an item in a tab control header. It's up to each implementation
// to decide what states to support (active selection, selection, etc)
export const box_background_color = background_color
export const box_alt_background_color = Colors.getColor('gray', '100')

/**
 * Background color for skeleton or "loading" boxes
 */
export const box_skeleton_background_color = Colors.getColor('gray', '200')

export function skeleton_background_gradient(parent, color) {
    return Qt.createQmlObject(`import QtQuick 2.12;
    Gradient{
        orientation:Gradient.Horizontal
        GradientStop{position:0.0;color:'${Colors.hexPlusAlpha(color, 0.0)}'}
        GradientStop{position:0.5;color:'${Colors.hexPlusAlpha(color, 0.5)}'}
        GradientStop{position:1.0;color:'${Colors.hexPlusAlpha(color, 0.0)}'}
    }`, parent)
}

export const box_border_color = Colors.getColor('gray', '200')
export const box_border_accent_color = Colors.blue
export const box_selected_background_color = '#ebeef1'
export const box_hover_text_color = Colors.getColor('gray', '900')
export const box_selected_text_color = Colors.getColor('gray', '900')
export const box_selected_border_color = Colors.getColor('gray', '400')
export const box_selected_active_background_color = Colors.blue
export const box_selected_active_text_color = Colors.white
export const box_selected_selected_active_border_color = Colors.getColor('gray', '400')
export const box_placeholder_color = Colors.getColor('gray', '500')

export const co_author_tag_background_color = Colors.getColor('blue', '000')
export const co_author_tag_border_color = Colors.getColor('blue', '200')

export const win32_title_bar_height = 28
export const win32_title_bar_background_color = Colors.getColor('gray', '900')

export const darwin_title_bar_height = 22

export const spacing = 10
export const spacingX2 = spacing * 2
export const spacingX4 = spacing * 3
export const spacingX5 = spacing * 3
export const spacing_half = spacing / 2
export const spacing_third = spacing / 3

export const border_radius = 3
export const base_border_width = 1
export const base_border_color = box_border_color

export const shadow_color = '#47535f'
export const base_box_shadow = {
    horizontalOffset: 0,
    verticalOffset: 2,
    radius: 7,
    color: shadow_color
}

export const toolbar_height = 50
export const toolbar_background_color = Colors.getColor('gray', '900')
export const toolbar_text_color = Colors.getColor('gray', '900')
export const toolbar_text_secondary_color = Colors.getColor('gray', '300')
export const toolbar_button_background_color = 'transparent'
export const toolbar_button_border_color = '#000'
export const toolbar_button_secondary_color = toolbar_text_secondary_color
export const toolbar_button_hover_color = Colors.white
export const toolbar_button_hover_background_color = Colors.getColor('gray', '800')
export const toolbar_button_hover_border_color = toolbar_button_border_color
export const toolbar_button_focus_background_color = Colors.getColor('gray', '800')
export const toolbar_button_active_color = text_color
export const toolbar_button_active_background_color = background_color
export const toolbar_button_active_border_color = background_color
export const toolbar_button_progress_color = Colors.getColor('gray', '800')
export const toolbar_button_focus_progress_color = Colors.getColor('gray', '700')
export const toolbar_button_hover_progress_color = Colors.getColor('gray', '700')
export const toolbar_dropdown_open_progress_color = Colors.getColor('gray', '200')

/**
 * App menu bar colors (Windows/Linux only)
 */
export const app_menu_button_color = toolbar_text_color
export const app_menu_button_hover_color = toolbar_button_hover_color
export const app_menu_button_hover_background_color = toolbar_button_hover_background_color
export const app_menu_button_active_color = toolbar_button_active_color
export const app_menu_button_active_background_color = toolbar_button_active_background_color
export const app_menu_pane_color = text_color
export const app_menu_pane_secondary_color = text_secondary_color
export const app_menu_pane_background_color = toolbar_button_active_background_color
export const app_menu_divider_color = box_border_color

/**
 * Background color for badges inside of toolbar buttons.
 * Examples of badges are the ahead/behind bubble in the
 * push/pull button and the PR badge in the branch drop
 * down button.
 */
export const toolbar_badge_background_color = Colors.getColor('gray', '600')
export const toolbar_badge_active_background_color = Colors.getColor('gray', '200')

export const tab_bar_height = 29
export const tab_bar_active_color = Colors.blue
export const tab_bar_background_color = Colors.white
export const tab_bar_hover_background_color = Colors.getColor('gray', '100')

// Count bubble colors when used inside of a tab bar item
export const tab_bar_count_color = text_color
export const tab_bar_count_background_color = Colors.getColor('gray', '200')

/**
 * Badge colors when used inside of list items.
 * Example of this is the change indicators inside
 * of the repository list.
 */
export const list_item_badge_color = Colors.getColor('gray', '800')
export const list_item_badge_background_color = Colors.getColor('gray', '200')
export const list_item_selected_badge_color = Colors.getColor('gray', '900')
export const list_item_selected_badge_background_color = Colors.getColor('gray', '300')
export const list_item_selected_active_badge_color = Colors.getColor('gray', '900')
export const list_item_selected_active_badge_background_color = Colors.white
export const list_item_hover_background_color = Colors.getColor('gray', '100')

export const win32_scroll_bar_size = 10

export const toast_notification_color = Colors.getColor('gray', '000')
export const toast_notification_background_color = Colors.hexPlusAlpha(Colors.getColor('gray', '900'), 0.6)

export const tip_box_background_color = Colors.hexPlusAlpha(Colors.getColor('blue', '500'), 0.06)
export const tip_box_border_color = Colors.getColor('blue', '200')

/**The highlight color used for focus rings and focus box shadows */
export const focus_color = Colors.blue

export const text_field_height = 25
export const text_field_focus_shadow_color = Colors.hexPlusAlpha(Colors.blue, 0.25)

/**
 * Blankslate actions, see `BlankslateAction` component.
 */
export const primary_blankslate_action_background = Colors.getColor('blue', '000')
export const primary_blankslate_action_border_color = Colors.getColor('blue', '200')

/**
 * Diff view
 */
export const diff_line_padding_y = 2
export const diff_text_color = Colors.getColor('gray', '900')
export const diff_border_color = Colors.getColor('gray', '200')
export const diff_gutter_color = Colors.getColor('gray', '200')
export const diff_gutter_background_color = background_color
export const diff_line_number_color = Colors.getColor('gray', '700')
export const diff_line_number_column_width = 50
export const diff_selected_background_color = Colors.getColor('blue', '400')
export const diff_selected_border_color = Colors.getColor('blue', '600')
export const diff_selected_gutter_color = Colors.getColor('blue', '600')
export const diff_selected_text_color = background_color
export const diff_add_background_color = Colors.darken(Colors.getColor('green', '000'), 0.02)
export const diff_add_border_color = Colors.getColor('green', '300')
export const diff_add_gutter_color = Colors.getColor('green', '300')
export const diff_add_gutter_background_color = Colors.darken(Colors.getColor('green', '100'), 0.03)
export const diff_add_inner_background_color = '#acf2bd'
export const diff_add_text_color = diff_text_color
export const diff_delete_background_color = Colors.getColor('red', '000')
export const diff_delete_border_color = Colors.getColor('red', '200')
export const diff_delete_gutter_color = Colors.getColor('red', '200')
export const diff_delete_gutter_background_color = Colors.getColor('red', '100')
export const diff_delete_inner_background_color = '#fdb8c0'
export const diff_delete_text_color = diff_text_color

export const diff_hunk_background_color = Colors.getColor('blue', '000')
export const diff_hunk_border_color = Colors.getColor('blue', '200')
export const diff_hunk_gutter_color = Colors.darken(Colors.getColor('blue', '200'), 0.05)
export const diff_hunk_gutter_background_color = Colors.getColor('blue', '100')
export const diff_hunk_text_color = Colors.gray

export const diff_hover_background_color = Colors.getColor('blue', '300')
export const diff_hover_border_color = Colors.getColor('blue', '400')
export const diff_hover_gutter_color = Colors.getColor('blue', '400')
export const diff_hover_text_color = background_color

export const diff_add_hover_background_color = Colors.getColor('green', '300')
export const diff_add_hover_border_color = Colors.getColor('green', '400')
export const diff_add_hover_gutter_color = Colors.getColor('green', '400')
export const diff_add_hover_text_color = text_color

export const diff_delete_hover_background_color = Colors.getColor('red', '200')
export const diff_delete_hover_border_color = Colors.getColor('red', '300')
export const diff_delete_hover_gutter_color = Colors.getColor('red', '300')
export const diff_delete_hover_text_color = text_color

// Syntax highlighting text colors
export const syntax_variable_color = '#6f42c1'
export const syntax_alt_variable_color = '#24292e'
export const syntax_keyword_color = '#d73a49'
export const syntax_atom_color = '#005cc5'
export const syntax_string_color = '#032f62'
export const syntax_qualifier_color = '#6f42c1'
export const syntax_type_color = '#d73a49'
export const syntax_comment_color = Colors.getColor('gray', '500')
export const syntax_tag_color = '#22863a'
export const syntax_attribute_color = '#6f42c1'
export const syntax_link_color = '#032f62'
export const syntax_header_color = '#0000ff'

export const undo_animation_duration = 500

// Colors for form errors
export const error_color = Colors.red
export const form_error_background = Colors.getColor('red', '100')
export const form_error_border_color = Colors.getColor('red', '200')
export const form_error_text_color = Colors.getColor('red', '800')


// Dialog
export const dialog_warning_color = Colors.getColor('yellow','600')
export const dialog_error_color = Colors.red

// Inline paths and code
export const path_segment_background = Colors.getColor('blue','000')
export const path_segment_padding = spacing_third

// Diverging notification banner colors
export const notification_banner_background = Colors.getColor('blue','000')
export const notification_banner_background_color = Colors.getColor('blue','200')
export const notification_ref_background = Colors.hexPlusAlpha('#fff',0.75)
export const dialog_rebase_progress_background = Colors.green

// merge/rebase status indicators
export const status_pending_color = Colors.getColor('yellow','700')
export const status_error_color = Colors.getColor('red','500')
export const status_success_color = Colors.getColor('green','500')

// Typography
export const font_weight_semibold = 600
export const font_weight_light = 300

// Pixels
export const font_size = 12
export const font_size_sm = 11
export const font_size_md = 14
export const font_size_lg = 28
export const font_size_xl = 32
export const font_size_xxl = 42
export const font_size_xs = 9
